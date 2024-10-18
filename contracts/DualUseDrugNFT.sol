// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract DualUseDrugNFT is ERC721, Ownable {
    uint256 public nextTokenId;

    constructor() ERC721("DualUseDrugNFT", "DUDNFT") {}

    function mintNFT(address recipient, string memory metadata) public onlyOwner {
        uint256 tokenId = nextTokenId;
        nextTokenId++;
        _mint(recipient, tokenId);
        // Add logic for storing metadata in real use cases.
    }
}
