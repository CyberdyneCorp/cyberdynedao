// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";

contract CyberdyneProducts is Ownable {
    struct Product {
        string uuid;
        string title;
        uint256 categoryId;
        uint256 priceUSDC; // Price in USDC (6 decimals)
        string ipfsLocation; // IPFS hash for additional content
        address creator; // Address that created this product
        uint256 createdAt;
        uint256 updatedAt;
        bool isActive; // Product availability status
        bool exists;
    }

    struct Category {
        uint256 id;
        string name;
        string description;
        uint256 createdAt;
        bool exists;
    }

    // State variables
    mapping(uint256 => Category) public categories;
    mapping(string => Product) public products; // uuid => Product
    mapping(uint256 => string[]) public categoryProducts; // categoryId => uuid[]
    mapping(address => string[]) public productsByCreator; // creator => uuid[]
    mapping(address => bool) public authorizedCreators; // Whitelist of addresses that can create products
    
    uint256 public nextCategoryId;
    string[] public allProductUuids;
    address[] public authorizedCreatorsList; // Array to track all authorized creators

    // Events
    event CategoryCreated(uint256 indexed categoryId, string name, string description);
    event ProductCreated(
        string uuid,
        string title,
        uint256 indexed categoryId,
        uint256 priceUSDC,
        string ipfsLocation,
        address indexed creator
    );
    event ProductUpdated(
        string indexed uuid,
        string title,
        uint256 indexed categoryId,
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
        nextCategoryId = 1;
        
        // Automatically authorize the contract owner
        authorizedCreators[msg.sender] = true;
        authorizedCreatorsList.push(msg.sender);
    }

    // Modifiers
    modifier validCategory(uint256 categoryId) {
        require(categories[categoryId].exists, "Category does not exist");
        _;
    }

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
            msg.sender,
            _title,
            allProductUuids.length, // replaces totalProducts
            blockhash(block.number - 1) // changing salt for better uniqueness
        ));
        
        // Convert to hex string in standard UUID format: 8-4-4-4-12
        return string(abi.encodePacked(
            _toHexString(uint256(hash) >> 224, 8), "-",
            _toHexString(uint256(uint16(uint256(hash) >> 208)), 4), "-",
            _toHexString(uint256(uint16(uint256(hash) >> 192)), 4), "-",
            _toHexString(uint256(uint16(uint256(hash) >> 176)), 4), "-",
            _toHexString(uint256(uint48(uint256(hash) >> 128)), 12)
        ));
    }

    // Helper function to convert hex nibble to character
    function _hexNibble(uint8 nib) private pure returns (bytes1) {
        return bytes1(nib + (nib < 10 ? 48 : 87));
    }

    // Helper function to convert uint to hex string
    function _toHexString(uint256 value, uint256 length) internal pure returns (string memory) {
        bytes memory buffer = new bytes(length);
        for (uint256 i = length; i > 0; ) {
            buffer[i - 1] = _hexNibble(uint8(value & 0x0f));
            value >>= 4;
            unchecked { --i; }
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


    // Category management functions (owner or authorized creators)
    function createCategory(
        string memory _name,
        string memory _description
    ) external onlyAuthorizedCreator returns (uint256) {
        require(bytes(_name).length > 0, "Category name cannot be empty");
        
        uint256 categoryId = nextCategoryId;
        categories[categoryId] = Category({
            id: categoryId,
            name: _name,
            description: _description,
            createdAt: block.timestamp,
            exists: true
        });
        
        nextCategoryId++;
        
        emit CategoryCreated(categoryId, _name, _description);
        return categoryId;
    }

    // Product management functions (authorized creators only)
    function createProduct(
        string memory _title,
        uint256 _categoryId,
        uint256 _priceUSDC,
        string memory _ipfsLocation
    ) external onlyAuthorizedCreator validCategory(_categoryId) returns (string memory) {
        require(bytes(_title).length > 0, "Title cannot be empty");
        require(_priceUSDC > 0, "Price must be greater than 0");
        require(bytes(_ipfsLocation).length > 0, "IPFS location cannot be empty");

        // Generate UUID based on current block and title
        string memory _uuid = generateUuid(_title);
        require(!products[_uuid].exists, "Generated UUID already exists (very unlikely)");

        products[_uuid] = Product({
            uuid: _uuid,
            title: _title,
            categoryId: _categoryId,
            priceUSDC: _priceUSDC,
            ipfsLocation: _ipfsLocation,
            creator: msg.sender,
            createdAt: block.timestamp,
            updatedAt: block.timestamp,
            isActive: true,
            exists: true
        });

        categoryProducts[_categoryId].push(_uuid);
        productsByCreator[msg.sender].push(_uuid);
        allProductUuids.push(_uuid);

        emit ProductCreated(_uuid, _title, _categoryId, _priceUSDC, _ipfsLocation, msg.sender);
        
        return _uuid;
    }

    // Update product (owner or creator only)
    function updateProduct(
        string memory _uuid,
        string memory _title,
        uint256 _categoryId,
        uint256 _priceUSDC,
        string memory _ipfsLocation
    ) external onlyOwnerOrCreator(_uuid) validCategory(_categoryId) {
        require(bytes(_title).length > 0, "Title cannot be empty");
        require(_priceUSDC > 0, "Price must be greater than 0");
        require(bytes(_ipfsLocation).length > 0, "IPFS location cannot be empty");

        Product storage product = products[_uuid];
        uint256 oldCategoryId = product.categoryId;
        
        // If category is changing, update category mappings
        if (oldCategoryId != _categoryId) {
            // Remove from old category
            string[] storage oldCategoryProds = categoryProducts[oldCategoryId];
            for (uint256 i = 0; i < oldCategoryProds.length; i++) {
                if (keccak256(abi.encodePacked(oldCategoryProds[i])) == keccak256(abi.encodePacked(_uuid))) {
                    oldCategoryProds[i] = oldCategoryProds[oldCategoryProds.length - 1];
                    oldCategoryProds.pop();
                    break;
                }
            }
            
            // Add to new category
            categoryProducts[_categoryId].push(_uuid);
        }
        
        product.title = _title;
        product.categoryId = _categoryId;
        product.priceUSDC = _priceUSDC;
        product.ipfsLocation = _ipfsLocation;
        product.updatedAt = block.timestamp;

        emit ProductUpdated(_uuid, _title, _categoryId, _priceUSDC, _ipfsLocation, msg.sender);
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
        uint256 categoryId = product.categoryId;
        address creator = product.creator;
        
        // Mark as deleted (set exists to false)
        product.exists = false;
        
        // Remove from category products array
        string[] storage categoryProds = categoryProducts[categoryId];
        for (uint256 i = 0; i < categoryProds.length; i++) {
            if (keccak256(abi.encodePacked(categoryProds[i])) == keccak256(abi.encodePacked(_uuid))) {
                categoryProds[i] = categoryProds[categoryProds.length - 1];
                categoryProds.pop();
                break;
            }
        }
        
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
    function getCategory(uint256 _categoryId) external view validCategory(_categoryId) returns (Category memory) {
        return categories[_categoryId];
    }

    function getProduct(string memory _uuid) external view returns (Product memory) {
        require(products[_uuid].exists, "Product does not exist");
        return products[_uuid];
    }

    function getProductsByCategory(uint256 _categoryId) 
        external 
        view 
        validCategory(_categoryId) 
        returns (Product[] memory) 
    {
        string[] memory uuids = categoryProducts[_categoryId];
        Product[] memory categoryProds = new Product[](uuids.length);
        
        for (uint256 i = 0; i < uuids.length; i++) {
            categoryProds[i] = products[uuids[i]];
        }
        
        return categoryProds;
    }

    function getCategoryProductCount(uint256 _categoryId) 
        external 
        view 
        validCategory(_categoryId) 
        returns (uint256) 
    {
        return categoryProducts[_categoryId].length;
    }

    function getAllCategories() external view returns (Category[] memory) {
        Category[] memory allCategories = new Category[](nextCategoryId - 1);
        uint256 index = 0;
        
        for (uint256 i = 1; i < nextCategoryId; i++) {
            if (categories[i].exists) {
                allCategories[index] = categories[i];
                index++;
            }
        }
        
        // Resize array to actual count
        Category[] memory result = new Category[](index);
        for (uint256 i = 0; i < index; i++) {
            result[i] = allCategories[i];
        }
        
        return result;
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
        uint256 n = allProductUuids.length;
        Product[] memory out = new Product[](n);
        for (uint256 i = 0; i < n; ) {
            out[i] = products[allProductUuids[i]];
            unchecked { ++i; }
        }
        return out;
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

    function getTotalProductCount() external view returns (uint256) {
        return allProductUuids.length;
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

    function categoryExists(uint256 _categoryId) external view returns (bool) {
        return categories[_categoryId].exists;
    }
}