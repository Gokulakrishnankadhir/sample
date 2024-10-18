# app.py
'''
from flask import Flask, request, jsonify
from web3 import Web3
import json
import os

app = Flask(__name__)

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Connect to Polygon network
polygon_rpc_url = os.getenv('POLYGON_RPC_URL')
web3 = Web3(Web3.HTTPProvider(polygon_rpc_url))

# Load contract
with open('/Users/kirthika/Desktop/drug_track/backend/contract_abi.json', 'r') as f:
    contract_abi = json.load(f)


contract_address = os.getenv('CONTRACT_ADDRESS')
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

private_key = os.getenv('PRIVATE_KEY')

# Route for creating NFT
@app.route('/create-nft', methods=['POST'])
def create_nft():
    data = request.json
    destination = data.get('destination')
    units = data.get('units')
    drug_type = data.get('drugType')

    try:
        account = web3.eth.account.from_key(private_key)
        tx = contract.functions.mintNFT(
            account.address,
            json.dumps({"units": units, "destination": destination, "drugType": drug_type})
        ).buildTransaction({
            'from': account.address,
            'nonce': web3.eth.getTransactionCount(account.address),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei')
        })

        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        return jsonify(success=True, nftHash=web3.toHex(tx_hash))

    except Exception as e:
        return jsonify(success=False, error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
'''
'''
from flask import Flask, request, jsonify, render_template, url_for
from web3 import Web3
import json
import os

# Create the Flask app and specify static and template folder paths
app = Flask(__name__, static_folder='/Users/kirthika/Desktop/drug_track/frontend/static', template_folder='/Users/kirthika/Desktop/drug_track/frontend/templates')

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Connect to Polygon network using the environment variable
polygon_rpc_url = os.getenv('POLYGON_RPC_URL')
if not polygon_rpc_url:
    raise EnvironmentError("POLYGON_RPC_URL is not set in the environment variables.")
web3 = Web3(Web3.HTTPProvider(polygon_rpc_url))

# Load the contract ABI from a JSON file
contract_abi_path = '/Users/kirthika/Desktop/drug_track/backend/contract_abi.json'
if not os.path.exists(contract_abi_path):
    raise FileNotFoundError(f"Contract ABI file not found at {contract_abi_path}")

with open(contract_abi_path, 'r') as f:
    contract_abi = json.load(f)

# Get the contract address from environment variables
contract_address = os.getenv('CONTRACT_ADDRESS')
if not contract_address:
    raise EnvironmentError("CONTRACT_ADDRESS is not set in the environment variables.")
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Get the private key from environment variables (for signing transactions)
private_key = os.getenv('PRIVATE_KEY')
if not private_key:
    raise EnvironmentError("PRIVATE_KEY is not set in the environment variables.")

# Sample users for authentication (you can replace this with a database)
users = {
    'manufacturer@test.com': 'password123',
    'supplier@test.com': 'password123',
    'distributor@test.com': 'password123'
}

# Route for the login page
# Route for the login page
@app.route('/')
def login():
    return render_template('/login.html')
# Route to handle login authentication
@app.route('/login', methods=['POST'])
def handle_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if email in users and users[email] == password:
        return jsonify(success=True)
    return jsonify(success=False, message="Invalid credentials")

# Route for the delivery page
@app.route('/delivery')
def delivery():
    return render_template('delivery.html')

# Route to create an NFT based on delivery information
@app.route('/create-nft', methods=['POST'])
def create_nft():
    try:
        # Get data from the request
        data = request.json
        destination = data.get('destination')
        units = data.get('units')
        drug_type = data.get('drugType')

        if not destination or not units or not drug_type:
            return jsonify(success=False, error="Missing parameters"), 400

        # Interact with the blockchain to mint the NFT
        account = web3.eth.account.from_key(private_key)

        # Log the transaction details
        print(f"Minting NFT for: {account.address}, Destination: {destination}, Units: {units}, Drug Type: {drug_type}")

        # Send the transaction to mint NFT
        tx = contract.functions.mintNFT(
            account.address,  # The address of the recipient (account creating the NFT)
            json.dumps({"units": units, "destination": destination, "drugType": drug_type})
        ).transact({
            'from': account.address,
            'gas': 2000000,
            'gasPrice': web3.eth.gas_price  # Use the current gas price from web3.eth
        })

        # Return the transaction hash
        return jsonify(success=True, txHash=web3.toHex(tx))

    except ValueError as ve:
        # Log the specific blockchain error
        print(f"Blockchain error: {ve}")
        return jsonify(success=False, error=f"Blockchain error: {str(ve)}"), 400

    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error: {e}")
        return jsonify(success=False, error=f"Unexpected error: {str(e)}"), 500

if __name__ == '__main__':
    app.run(debug=True)
'''
'''
from flask import Flask, request, jsonify, render_template
from web3 import Web3
import json
import os
import qrcode
import hashlib
from io import BytesIO
import base64

# Create the Flask app and specify static and template folder paths
app = Flask(__name__, static_folder='/Users/kirthika/Desktop/drug_track/frontend/static', template_folder='/Users/kirthika/Desktop/drug_track/frontend/templates')

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Connect to Polygon network using the environment variable
polygon_rpc_url = os.getenv('POLYGON_RPC_URL')
if not polygon_rpc_url:
    raise EnvironmentError("POLYGON_RPC_URL is not set in the environment variables.")
web3 = Web3(Web3.HTTPProvider(polygon_rpc_url))

# Load the contract ABI from a JSON file
contract_abi_path = '/Users/kirthika/Desktop/drug_track/backend/contract_abi.json'
if not os.path.exists(contract_abi_path):
    raise FileNotFoundError(f"Contract ABI file not found at {contract_abi_path}")

with open(contract_abi_path, 'r') as f:
    contract_abi = json.load(f)

# Get the contract address from environment variables
contract_address = os.getenv('CONTRACT_ADDRESS')
if not contract_address:
    raise EnvironmentError("CONTRACT_ADDRESS is not set in the environment variables.")
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Get the private key from environment variables (for signing transactions)
private_key = os.getenv('PRIVATE_KEY')
if not private_key:
    raise EnvironmentError("PRIVATE_KEY is not set in the environment variables.")

# Sample users for authentication (you can replace this with a database)
users = {
    'manufacturer@test.com': 'password123',
    'supplier@test.com': 'password123',
    'distributor@test.com': 'password123'
}

# Route for the login page
@app.route('/')
def login():
    return render_template('login.html')

# Route to handle login authentication
@app.route('/login', methods=['POST'])
def handle_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if email in users and users[email] == password:
        return jsonify(success=True)
    return jsonify(success=False, message="Invalid credentials")

# Route for the delivery page
@app.route('/delivery')
def delivery():
    return render_template('delivery.html')

# Route to create an NFT based on delivery information
@app.route('/create-nft', methods=['POST'])
def create_nft():
    try:
        # Get data from the request
        data = request.json
        destination = data.get('destination')
        units = data.get('units')
        drug_type = data.get('drugType')

        if not destination or not units or not drug_type:
            return jsonify(success=False, error="Missing parameters"), 400

        # Interact with the blockchain to mint the NFT
        account = web3.eth.account.from_key(private_key)

        # Log the transaction details
        print(f"Minting NFT for: {account.address}, Destination: {destination}, Units: {units}, Drug Type: {drug_type}")

        # Send the transaction to mint NFT
        tx = contract.functions.mintNFT(
            account.address,  # The address of the recipient (account creating the NFT)
            json.dumps({"units": units, "destination": destination, "drugType": drug_type})
        ).transact({
            'from': account.address,
            'gas': 2000000,
            'gasPrice': web3.eth.gas_price  # Use the current gas price from web3.eth
        })

        # Generate a 32-byte hash of the transaction details for the QR code
        transaction_data = f"{account.address}-{destination}-{units}-{drug_type}-{web3.toHex(tx)}"
        hash_object = hashlib.sha256(transaction_data.encode())
        transaction_hash = hash_object.hexdigest()[:64]  # Get the first 64 characters (32 bytes in hex)

        # Generate QR code with the transaction hash
        qr = qrcode.make(transaction_hash)
        
        # Save QR code to a BytesIO object
        qr_buffer = BytesIO()
        qr.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        
        # Encode QR code as base64
        qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode('utf-8')
        qr_url = f"data:image/png;base64,{qr_base64}"

        # Return the transaction hash and QR code URL
        return jsonify(success=True, txHash=web3.toHex(tx), qrCodeUrl=qr_url)

    except ValueError as ve:
        # Log the specific blockchain error
        print(f"Blockchain error: {ve}")
        return jsonify(success=False, error=f"Blockchain error: {str(ve)}"), 400

    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error: {e}")
        return jsonify(success=False, error=f"Unexpected error: {str(e)}"), 500

if __name__ == '__main__':
    app.run(debug=True)
'''
from flask import Flask, request, jsonify, render_template
from web3 import Web3
import json
import os
import qrcode
import hashlib
from io import BytesIO
import base64

# Create the Flask app and specify static and template folder paths
app = Flask(__name__, static_folder='/Users/kirthika/Desktop/drug_track/frontend/static', template_folder='/Users/kirthika/Desktop/drug_track/frontend/templates')

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Connect to Polygon network using the environment variable
polygon_rpc_url = os.getenv('POLYGON_RPC_URL')
if not polygon_rpc_url:
    raise EnvironmentError("POLYGON_RPC_URL is not set in the environment variables.")
web3 = Web3(Web3.HTTPProvider(polygon_rpc_url))

# Load the contract ABI from a JSON file
contract_abi_path = '/Users/kirthika/Desktop/drug_track/backend/contract_abi.json'
if not os.path.exists(contract_abi_path):
    raise FileNotFoundError(f"Contract ABI file not found at {contract_abi_path}")

with open(contract_abi_path, 'r') as f:
    contract_abi = json.load(f)

# Get the contract address from environment variables
contract_address = os.getenv('CONTRACT_ADDRESS')
if not contract_address:
    raise EnvironmentError("CONTRACT_ADDRESS is not set in the environment variables.")
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Get the private key from environment variables (for signing transactions)
private_key = os.getenv('PRIVATE_KEY')
if not private_key:
    raise EnvironmentError("PRIVATE_KEY is not set in the environment variables.")

# Sample users for authentication (you can replace this with a database)
users = {
    'manufacturer@test.com': 'password123',
    'supplier@test.com': 'password123',
    'distributor@test.com': 'password123'
}

# Route for the login page
@app.route('/')
def login():
    return render_template('login.html')

# Route to handle login authentication
@app.route('/login', methods=['POST'])
def handle_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if email in users and users[email] == password:
        return jsonify(success=True)
    return jsonify(success=False, message="Invalid credentials")

# Route for the delivery page
@app.route('/delivery')
def delivery():
    return render_template('delivery.html')

# Route to create an NFT based on delivery information
@app.route('/create-nft', methods=['POST'])
def create_nft():
    try:
        # Get data from the request
        data = request.json
        destination = data.get('destination')
        units = data.get('units')
        drug_type = data.get('drugType')

        if not destination or not units or not drug_type:
            return jsonify(success=False, error="Missing parameters"), 400

        # Interact with the blockchain to mint the NFT
        account = web3.eth.account.from_key(private_key)

        # Log the transaction details
        print(f"Minting NFT for: {account.address}, Destination: {destination}, Units: {units}, Drug Type: {drug_type}")

        # Get the current nonce
        nonce = web3.eth.getTransactionCount(account.address)

        # Build the transaction dictionary
        transaction = {
            'from': account.address,
            'gas': 2000000,
            'gasPrice': web3.eth.gas_price,  # Use the current gas price from web3.eth
            'nonce': nonce,
        }

        # Send the transaction to mint NFT
        tx_hash = contract.functions.mintNFT(
            account.address,  # The address of the recipient (account creating the NFT)
            json.dumps({"units": units, "destination": destination, "drugType": drug_type})
        ).transact(transaction)

        # Generate a 32-byte hash of the transaction details for the QR code
        transaction_data = f"{account.address}-{destination}-{units}-{drug_type}-{web3.toHex(tx_hash)}"
        hash_object = hashlib.sha256(transaction_data.encode())
        transaction_hash = hash_object.hexdigest()[:64]  # Get the first 64 characters (32 bytes in hex)

        # Generate QR code with the transaction hash
        qr = qrcode.make(transaction_hash)
        
        # Save QR code to a BytesIO object
        qr_buffer = BytesIO()
        qr.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        
        # Encode QR code as base64
        qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode('utf-8')
        qr_url = f"data:image/png;base64,{qr_base64}"

        # Return the transaction hash and QR code URL
        return jsonify(success=True, txHash=web3.toHex(tx_hash), qrCodeUrl=qr_url)

    except ValueError as ve:
        # Log the specific blockchain error
        print(f"Blockchain error: {ve}")
        return jsonify(success=False, error=f"Blockchain error: {str(ve)}"), 400

    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error: {e}")
        return jsonify(success=False, error=f"Unexpected error: {str(e)}"), 500

if __name__ == '__main__':
    app.run(debug=True)
