// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract ReaderEditionNFT is ERC721, ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;

    uint256 public constant MAX_PER_WALLET = 5;
    uint256 public constant TOTAL_SUPPLY = 100;

    Counters.Counter private _tokenIdCounter;

    mapping(address => uint256) public mintedPerWallet;

    string private _baseTokenURI;

    constructor(address initialOwner) 
        ERC721("Bithues Reader's Edition", "BITHUES")
        Ownable(initialOwner)
    {
        _baseTokenURI = "ipfs://QmYourCIDHere/metadata/";
    }

    function mint(address to) external onlyOwner {
        require(_tokenIdCounter.current() < TOTAL_SUPPLY, "Max supply reached");
        require(mintedPerWallet[to] < MAX_PER_WALLET, "Max per wallet reached");

        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        mintedPerWallet[to]++;

        _safeMint(to, tokenId);
    }

    function batchMint(address[] calldata recipients) external onlyOwner {
        require(_tokenIdCounter.current() + recipients.length <= TOTAL_SUPPLY, "Exceeds max supply");

        for (uint256 i = 0; i < recipients.length; i++) {
            require(mintedPerWallet[recipients[i]] < MAX_PER_WALLET, "Wallet limit");
            uint256 tokenId = _tokenIdCounter.current();
            _tokenIdCounter.increment();
            mintedPerWallet[recipients[i]]++;
            _safeMint(recipients[i], tokenId);
        }
    }

    function tokenURI(uint256 tokenId)
        public view override(ERC721, ERC721URIStorage) returns (string memory)
    {
        require(ownerOf(tokenId) != address(0), "Token does not exist");
        return string(abi.encodePacked(_baseTokenURI, Strings.toString(tokenId), ".json"));
    }

    function setBaseURI(string calldata newBaseURI) external onlyOwner {
        _baseTokenURI = newBaseURI;
    }

    function withdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }

    function supportsInterface(bytes4 interfaceId)
        public view override(ERC721, ERC721URIStorage) returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
