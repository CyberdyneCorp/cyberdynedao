// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";

contract CyberdyneProducts is Ownable {
    struct Product {
        string uuid;
        string title;
        uint256 priceUSDC; // Price in USDC (6 decimals)
        string ipfsLocation; // IPFS hash for additional content
        address creator; // Address that created this product
        uint256 createdAt;
        uint256 updatedAt;
        bool isActive; // Product availability status
        bool exists;
    }

    // State variables
    mapping(string => Product) public products; // uuid => Product
    mapping(address => string[]) public productsByCreator; // creator => uuid[]
    mapping(address => bool) public authorizedCreators; // Whitelist of addresses that can create products
    
    uint256 public totalProducts;
    string[] public allProductUuids;
    address[] public authorizedCreatorsList; // Array to track all authorized creators

    // Events
    event ProductCreated(
        string uuid,
        string title,
        uint256 priceUSDC,
        string ipfsLocation,
        address indexed creator
    );
    event ProductUpdated(
        string indexed uuid,
        string title,
        uint256 priceUSDC,
        string ipfsLocation,
        address indexed updatedBy
    );
    event ProductStatusChanged(
        string indexed uuid,
        bool isActive,
        address indexed changedBy
    );
    event ProductDeleted(string indexed uuid, address indexed deletedBy, address indexed creator);
    event CreatorAuthorized(address indexed creator, address indexed authorizedBy);
    event CreatorDeauthorized(address indexed creator, address indexed deauthorizedBy);
    event ContractOwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor() Ownable(msg.sender) {
        totalProducts = 0;
        
        // Automatically authorize the contract owner
        authorizedCreators[msg.sender] = true;
        authorizedCreatorsList.push(msg.sender);
    }

    // Modifiers
    modifier onlyAuthorizedCreator() {
        require(authorizedCreators[msg.sender], "Not authorized to create products");
        _;
    }

    modifier onlyOwnerOrCreator(string memory uuid) {
        require(products[uuid].exists, "Product does not exist");
        require(
            msg.sender == owner() || msg.sender == products[uuid].creator,
            "Only owner or creator can modify this product"
        );
        _;
    }


    // Helper function to generate UUID based on block data and title
    function generateUuid(string memory _title) internal view returns (string memory) {
        bytes32 hash = keccak256(abi.encodePacked(
            block.timestamp,
            block.prevrandao,
            block.number,
            msg.sender,
            _title,
            totalProducts
        ));
        
        // Convert to hex string and take first 32 characters for UUID-like format
        return string(abi.encodePacked(
            _toHexString(uint256(hash) >> 128, 16),
            "-",
            _toHexString(uint256(hash >> 96) & 0xFFFF, 4),
            "-",
            _toHexString(uint256(hash >> 80) & 0xFFFF, 4),
            "-",
            _toHexString(uint256(hash >> 64) & 0xFFFF, 4),
            "-",
            _toHexString(uint256(hash >> 16) & 0xFFFFFFFFFFFF, 12)
        ));
    }

    // Helper function to convert uint to hex string
    function _toHexString(uint256 value, uint256 length) internal pure returns (string memory) {
        bytes memory buffer = new bytes(length);
        for (uint256 i = length; i > 0; i--) {
            buffer[i - 1] = bytes1(uint8(value & 0xf) + (value & 0xf < 10 ? 48 : 87));
            value >>= 4;
        }
        return string(buffer);
    }

    // Creator whitelist management functions (owner only)
    function authorizeCreator(address _creator) external onlyOwner {
        require(_creator != address(0), "Cannot authorize zero address");
        require(!authorizedCreators[_creator], "Creator already authorized");
        
        authorizedCreators[_creator] = true;
        authorizedCreatorsList.push(_creator);
        
        emit CreatorAuthorized(_creator, msg.sender);
    }

    function deauthorizeCreator(address _creator) external onlyOwner {
        require(_creator != address(0), "Cannot deauthorize zero address");
        require(authorizedCreators[_creator], "Creator not authorized");
        require(_creator != owner(), "Cannot deauthorize contract owner");
        
        authorizedCreators[_creator] = false;
        
        // Remove from array (find and replace with last element)
        for (uint256 i = 0; i < authorizedCreatorsList.length; i++) {
            if (authorizedCreatorsList[i] == _creator) {
                authorizedCreatorsList[i] = authorizedCreatorsList[authorizedCreatorsList.length - 1];
                authorizedCreatorsList.pop();
                break;
            }
        }
        
        emit CreatorDeauthorized(_creator, msg.sender);
    }

    function isAuthorizedCreator(address _creator) external view returns (bool) {
        return authorizedCreators[_creator];
    }

    function getAuthorizedCreators() external view returns (address[] memory) {
        return authorizedCreatorsList;
    }


    // Product management functions (authorized creators only)
    function createProduct(
        string memory _title,
        uint256 _priceUSDC,
        string memory _ipfsLocation
    ) external onlyAuthorizedCreator returns (string memory) {
        require(bytes(_title).length > 0, "Title cannot be empty");
        require(_priceUSDC > 0, "Price must be greater than 0");
        require(bytes(_ipfsLocation).length > 0, "IPFS location cannot be empty");

        // Generate UUID based on current block and title
        string memory _uuid = generateUuid(_title);
        require(!products[_uuid].exists, "Generated UUID already exists (very unlikely)");

        products[_uuid] = Product({
            uuid: _uuid,
            title: _title,
            priceUSDC: _priceUSDC,
            ipfsLocation: _ipfsLocation,
            creator: msg.sender,
            createdAt: block.timestamp,
            updatedAt: block.timestamp,
            isActive: true,
            exists: true
        });

        productsByCreator[msg.sender].push(_uuid);
        allProductUuids.push(_uuid);
        totalProducts++;

        emit ProductCreated(_uuid, _title, _priceUSDC, _ipfsLocation, msg.sender);
        
        return _uuid;
    }

    // Update product (owner or creator only)
    function updateProduct(
        string memory _uuid,
        string memory _title,
        uint256 _priceUSDC,
        string memory _ipfsLocation
    ) external onlyOwnerOrCreator(_uuid) {
        require(bytes(_title).length > 0, "Title cannot be empty");
        require(_priceUSDC > 0, "Price must be greater than 0");
        require(bytes(_ipfsLocation).length > 0, "IPFS location cannot be empty");

        Product storage product = products[_uuid];
        product.title = _title;
        product.priceUSDC = _priceUSDC;
        product.ipfsLocation = _ipfsLocation;
        product.updatedAt = block.timestamp;

        emit ProductUpdated(_uuid, _title, _priceUSDC, _ipfsLocation, msg.sender);
    }

    // Toggle product active status (owner or creator only)
    function toggleProductStatus(string memory _uuid) external onlyOwnerOrCreator(_uuid) {
        Product storage product = products[_uuid];
        product.isActive = !product.isActive;
        product.updatedAt = block.timestamp;

        emit ProductStatusChanged(_uuid, product.isActive, msg.sender);
    }

    // Delete product (owner or creator only)
    function deleteProduct(string memory _uuid) external onlyOwnerOrCreator(_uuid) {
        Product storage product = products[_uuid];
        address creator = product.creator;
        
        // Mark as deleted (set exists to false)
        product.exists = false;
        
        // Remove from creator products array
        string[] storage creatorProducts = productsByCreator[creator];
        for (uint256 i = 0; i < creatorProducts.length; i++) {
            if (keccak256(abi.encodePacked(creatorProducts[i])) == keccak256(abi.encodePacked(_uuid))) {
                creatorProducts[i] = creatorProducts[creatorProducts.length - 1];
                creatorProducts.pop();
                break;
            }
        }
        
        // Remove from all products array
        for (uint256 i = 0; i < allProductUuids.length; i++) {
            if (keccak256(abi.encodePacked(allProductUuids[i])) == keccak256(abi.encodePacked(_uuid))) {
                allProductUuids[i] = allProductUuids[allProductUuids.length - 1];
                allProductUuids.pop();
                break;
            }
        }
        
        // Decrease total count
        totalProducts--;
        
        emit ProductDeleted(_uuid, msg.sender, creator);
    }

    // Transfer contract ownership and ensure new owner is authorized
    function transferContractOwnership(address _newOwner) external onlyOwner {
        require(_newOwner != address(0), "New owner cannot be zero address");
        require(_newOwner != owner(), "New owner cannot be the same as current owner");
        
        address previousOwner = owner();
        
        // Authorize new owner if not already authorized
        if (!authorizedCreators[_newOwner]) {
            authorizedCreators[_newOwner] = true;
            authorizedCreatorsList.push(_newOwner);
        }
        
        // Transfer ownership using OpenZeppelin's function
        _transferOwnership(_newOwner);
        
        emit ContractOwnershipTransferred(previousOwner, _newOwner);
    }

    // View functions
    function getProduct(string memory _uuid) external view returns (Product memory) {
        require(products[_uuid].exists, "Product does not exist");
        return products[_uuid];
    }


    function getProductsByCreator(address _creator) external view returns (Product[] memory) {
        string[] memory uuids = productsByCreator[_creator];
        Product[] memory creatorProducts = new Product[](uuids.length);
        
        for (uint256 i = 0; i < uuids.length; i++) {
            creatorProducts[i] = products[uuids[i]];
        }
        
        return creatorProducts;
    }

    function getAllProducts() external view returns (Product[] memory) {
        Product[] memory allProducts = new Product[](totalProducts);
        
        for (uint256 i = 0; i < allProductUuids.length; i++) {
            allProducts[i] = products[allProductUuids[i]];
        }
        
        return allProducts;
    }

    function getActiveProducts() external view returns (Product[] memory) {
        // First count active products
        uint256 activeCount = 0;
        for (uint256 i = 0; i < allProductUuids.length; i++) {
            if (products[allProductUuids[i]].isActive) {
                activeCount++;
            }
        }
        
        // Create array with correct size
        Product[] memory activeProducts = new Product[](activeCount);
        uint256 index = 0;
        
        // Fill array with active products
        for (uint256 i = 0; i < allProductUuids.length; i++) {
            if (products[allProductUuids[i]].isActive) {
                activeProducts[index] = products[allProductUuids[i]];
                index++;
            }
        }
        
        return activeProducts;
    }

    function productExists(string memory _uuid) external view returns (bool) {
        return products[_uuid].exists;
    }


    function getCreatorProductCount(address _creator) external view returns (uint256) {
        return productsByCreator[_creator].length;
    }

    function getActiveProductCount() external view returns (uint256) {
        uint256 activeCount = 0;
        for (uint256 i = 0; i < allProductUuids.length; i++) {
            if (products[allProductUuids[i]].isActive) {
                activeCount++;
            }
        }
        return activeCount;
    }
}