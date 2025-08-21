// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";

contract CyberdyneProducts is Ownable {
    struct Product {
        uint256 id;              // Simple incremental ID instead of UUID string
        string title;
        uint256 categoryId;
        uint256 priceUSDC;       // Price in USDC (6 decimals)
        string ipfsLocation;     // IPFS hash for additional content
        address creator;         // Address that created this product
        uint256 createdAt;
        uint256 updatedAt;
        bool isActive;           // Product availability status
        bool exists;
    }

    struct Category {
        uint256 id;
        string name;
        string description;
        uint256 createdAt;
        bool exists;
    }

    // Simplified state variables - using uint256 instead of string
    mapping(uint256 => Category) public categories;
    mapping(uint256 => Product) public products;           // id => Product (much simpler!)
    mapping(uint256 => uint256[]) public categoryProducts; // categoryId => productId[]
    mapping(address => uint256[]) public productsByCreator; // creator => productId[]
    mapping(address => bool) public authorizedCreators;
    
    uint256 public nextCategoryId;
    uint256 public nextProductId;                          // Simple counter instead of UUID generation
    uint256[] public allProductIds;                        // uint256[] instead of string[]
    address[] public authorizedCreatorsList;

    // Much simpler index mappings - no nested string mappings!
    mapping(uint256 => uint256) private allIndex;                    // productId -> index in allProductIds
    mapping(uint256 => mapping(uint256 => uint256)) private catIndex; // catId, productId -> index
    mapping(address => mapping(uint256 => uint256)) private creatorIndex; // creator, productId -> index
    mapping(address => uint256) private authIndex;

    // Simplified events
    event CategoryCreated(uint256 indexed categoryId, string name, string description);
    event ProductCreated(
        uint256 indexed productId,  // uint256 instead of string
        string title,
        uint256 indexed categoryId,
        uint256 priceUSDC,
        string ipfsLocation,
        address indexed creator
    );
    event ProductUpdated(
        uint256 indexed productId,  // uint256 instead of string
        string title,
        uint256 indexed categoryId,
        uint256 priceUSDC,
        string ipfsLocation,
        address indexed updatedBy
    );
    event ProductStatusChanged(
        uint256 indexed productId,  // uint256 instead of string
        bool isActive,
        address indexed changedBy
    );
    event ProductDeleted(uint256 indexed productId, address indexed deletedBy, address indexed creator);
    event CreatorAuthorized(address indexed creator, address indexed authorizedBy);
    event CreatorDeauthorized(address indexed creator, address indexed deauthorizedBy);

    constructor() Ownable(msg.sender) {
        nextCategoryId = 1;
        nextProductId = 1;       // Start product IDs at 1
        
        // Automatically authorize the contract owner
        authorizedCreators[msg.sender] = true;
        _pushAuth(msg.sender);
    }

    // Simplified modifiers
    modifier validCategory(uint256 categoryId) {
        require(categories[categoryId].exists, "Category does not exist");
        _;
    }

    modifier onlyAuthorizedCreator() {
        require(authorizedCreators[msg.sender], "Not authorized to create products");
        _;
    }

    modifier onlyOwnerOrAuthorizedCreatorOf(uint256 productId) {  // uint256 instead of string
        require(products[productId].exists, "Product does not exist");
        require(
            msg.sender == owner() ||
            (authorizedCreators[msg.sender] && msg.sender == products[productId].creator),
            "Only owner or authorized creator can modify this product"
        );
        _;
    }

    // Creator management
    function authorizeCreator(address _creator) external onlyOwner {
        require(_creator != address(0), "Cannot authorize zero address");
        require(!authorizedCreators[_creator], "Creator already authorized");
        
        authorizedCreators[_creator] = true;
        _pushAuth(_creator);
        
        emit CreatorAuthorized(_creator, msg.sender);
    }

    function deauthorizeCreator(address _creator) external onlyOwner {
        require(_creator != address(0), "Cannot deauthorize zero address");
        require(authorizedCreators[_creator], "Creator not authorized");
        require(_creator != owner(), "Cannot deauthorize contract owner");
        
        authorizedCreators[_creator] = false;
        _removeAuth(_creator);
        
        emit CreatorDeauthorized(_creator, msg.sender);
    }

    function isAuthorizedCreator(address _creator) external view returns (bool) {
        return authorizedCreators[_creator];
    }

    function getAuthorizedCreators() external view returns (address[] memory) {
        return authorizedCreatorsList;
    }

    // Category management
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

    // MUCH simpler product creation - no UUID generation!
    function createProduct(
        string memory _title,
        uint256 _categoryId,
        uint256 _priceUSDC,
        string memory _ipfsLocation
    ) external onlyAuthorizedCreator validCategory(_categoryId) returns (uint256) {
        require(bytes(_title).length > 0, "Title cannot be empty");
        require(_priceUSDC > 0, "Price must be greater than 0");
        require(bytes(_ipfsLocation).length > 0, "IPFS location cannot be empty");

        uint256 productId = nextProductId;  // Simply increment!
        nextProductId++;

        products[productId] = Product({
            id: productId,
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

        _pushCat(_categoryId, productId);
        _pushCreator(msg.sender, productId);
        _pushAll(productId);

        emit ProductCreated(productId, _title, _categoryId, _priceUSDC, _ipfsLocation, msg.sender);
        
        return productId;
    }

    // Update product (owner or creator only)
    function updateProduct(
        uint256 _productId,  // uint256 instead of string
        string memory _title,
        uint256 _categoryId,
        uint256 _priceUSDC,
        string memory _ipfsLocation
    ) external onlyOwnerOrAuthorizedCreatorOf(_productId) validCategory(_categoryId) {
        require(bytes(_title).length > 0, "Title cannot be empty");
        require(_priceUSDC > 0, "Price must be greater than 0");
        require(bytes(_ipfsLocation).length > 0, "IPFS location cannot be empty");

        Product storage product = products[_productId];
        uint256 oldCategoryId = product.categoryId;
        
        // If category is changing, update category mappings
        if (oldCategoryId != _categoryId) {
            _removeCat(oldCategoryId, _productId);
            _pushCat(_categoryId, _productId);
        }
        
        product.title = _title;
        product.categoryId = _categoryId;
        product.priceUSDC = _priceUSDC;
        product.ipfsLocation = _ipfsLocation;
        product.updatedAt = block.timestamp;

        emit ProductUpdated(_productId, _title, _categoryId, _priceUSDC, _ipfsLocation, msg.sender);
    }

    function toggleProductStatus(uint256 _productId) external onlyOwnerOrAuthorizedCreatorOf(_productId) {
        Product storage product = products[_productId];
        product.isActive = !product.isActive;
        product.updatedAt = block.timestamp;

        emit ProductStatusChanged(_productId, product.isActive, msg.sender);
    }

    function deleteProduct(uint256 _productId) external onlyOwnerOrAuthorizedCreatorOf(_productId) {
        Product storage product = products[_productId];
        uint256 categoryId = product.categoryId;
        address creator = product.creator;
        
        // Mark as deleted (set exists to false)
        product.exists = false;
        
        // Remove from all arrays using O(1) operations
        _removeCat(categoryId, _productId);
        _removeCreator(creator, _productId);
        _removeAll(_productId);
        
        emit ProductDeleted(_productId, msg.sender, creator);
    }

    // View functions
    function getCategory(uint256 _categoryId) external view validCategory(_categoryId) returns (Category memory) {
        return categories[_categoryId];
    }

    function getProduct(uint256 _productId) external view returns (Product memory) {
        require(products[_productId].exists, "Product does not exist");
        return products[_productId];
    }

    function getTotalProductCount() external view returns (uint256) {
        return allProductIds.length;
    }

    function productExists(uint256 _productId) external view returns (bool) {
        return products[_productId].exists;
    }

    function categoryExists(uint256 _categoryId) external view returns (bool) {
        return categories[_categoryId].exists;
    }

    // Additional view functions for API compatibility
    function getAllCategories() external view returns (Category[] memory) {
        uint256 count = 0;
        for (uint256 i = 1; i < nextCategoryId; i++) {
            if (categories[i].exists) {
                count++;
            }
        }
        
        Category[] memory allCategories = new Category[](count);
        uint256 index = 0;
        for (uint256 i = 1; i < nextCategoryId; i++) {
            if (categories[i].exists) {
                allCategories[index] = categories[i];
                index++;
            }
        }
        
        return allCategories;
    }

    function getAllProducts() external view returns (Product[] memory) {
        Product[] memory allProducts = new Product[](allProductIds.length);
        for (uint256 i = 0; i < allProductIds.length; i++) {
            allProducts[i] = products[allProductIds[i]];
        }
        return allProducts;
    }

    function getAllActiveProducts() external view returns (Product[] memory) {
        uint256 count = 0;
        for (uint256 i = 0; i < allProductIds.length; i++) {
            if (products[allProductIds[i]].isActive) {
                count++;
            }
        }
        
        Product[] memory activeProducts = new Product[](count);
        uint256 index = 0;
        for (uint256 i = 0; i < allProductIds.length; i++) {
            if (products[allProductIds[i]].isActive) {
                activeProducts[index] = products[allProductIds[i]];
                index++;
            }
        }
        
        return activeProducts;
    }

    function getAllProductsByCategory(uint256 _categoryId) external view validCategory(_categoryId) returns (Product[] memory) {
        uint256[] memory categoryProductIds = categoryProducts[_categoryId];
        Product[] memory categoryProductsArray = new Product[](categoryProductIds.length);
        
        for (uint256 i = 0; i < categoryProductIds.length; i++) {
            categoryProductsArray[i] = products[categoryProductIds[i]];
        }
        
        return categoryProductsArray;
    }

    function getAllProductsByCreator(address _creator) external view returns (Product[] memory) {
        uint256[] memory creatorProductIds = productsByCreator[_creator];
        Product[] memory creatorProductsArray = new Product[](creatorProductIds.length);
        
        for (uint256 i = 0; i < creatorProductIds.length; i++) {
            creatorProductsArray[i] = products[creatorProductIds[i]];
        }
        
        return creatorProductsArray;
    }

    function getCategoryProductCount(uint256 _categoryId) external view validCategory(_categoryId) returns (uint256) {
        return categoryProducts[_categoryId].length;
    }

    function getCreatorProductCount(address _creator) external view returns (uint256) {
        return productsByCreator[_creator].length;
    }

    function getActiveProductCount() external view returns (uint256) {
        uint256 count = 0;
        for (uint256 i = 0; i < allProductIds.length; i++) {
            if (products[allProductIds[i]].isActive) {
                count++;
            }
        }
        return count;
    }

    function transferContractOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "New owner cannot be zero address");
        require(newOwner != owner(), "New owner cannot be the same as current owner");
        
        // If the new owner is not already authorized, authorize them
        if (!authorizedCreators[newOwner]) {
            authorizedCreators[newOwner] = true;
            _pushAuth(newOwner);
        }
        
        transferOwnership(newOwner);
    }

    // Pagination functions
    function getProducts(uint256 offset, uint256 limit) external view returns (Product[] memory) {
        require(limit > 0, "Limit must be greater than 0");
        
        uint256 totalProducts = allProductIds.length;
        if (offset >= totalProducts) {
            return new Product[](0);
        }
        
        uint256 remainingProducts = totalProducts - offset;
        uint256 actualLimit = limit > remainingProducts ? remainingProducts : limit;
        
        Product[] memory paginatedProducts = new Product[](actualLimit);
        for (uint256 i = 0; i < actualLimit; i++) {
            paginatedProducts[i] = products[allProductIds[offset + i]];
        }
        
        return paginatedProducts;
    }

    function getProductsByCreator(address creator, uint256 offset, uint256 limit) external view returns (Product[] memory) {
        require(limit > 0, "Limit must be greater than 0");
        
        uint256[] memory creatorProductIds = productsByCreator[creator];
        uint256 totalProducts = creatorProductIds.length;
        
        if (offset >= totalProducts) {
            return new Product[](0);
        }
        
        uint256 remainingProducts = totalProducts - offset;
        uint256 actualLimit = limit > remainingProducts ? remainingProducts : limit;
        
        Product[] memory paginatedProducts = new Product[](actualLimit);
        for (uint256 i = 0; i < actualLimit; i++) {
            paginatedProducts[i] = products[creatorProductIds[offset + i]];
        }
        
        return paginatedProducts;
    }

    function getProductsByCategory(uint256 categoryId, uint256 offset, uint256 limit) external view validCategory(categoryId) returns (Product[] memory) {
        require(limit > 0, "Limit must be greater than 0");
        
        uint256[] memory categoryProductIds = categoryProducts[categoryId];
        uint256 totalProducts = categoryProductIds.length;
        
        if (offset >= totalProducts) {
            return new Product[](0);
        }
        
        uint256 remainingProducts = totalProducts - offset;
        uint256 actualLimit = limit > remainingProducts ? remainingProducts : limit;
        
        Product[] memory paginatedProducts = new Product[](actualLimit);
        for (uint256 i = 0; i < actualLimit; i++) {
            paginatedProducts[i] = products[categoryProductIds[offset + i]];
        }
        
        return paginatedProducts;
    }

    function getActiveProductsPaginated(uint256 offset, uint256 limit) external view returns (Product[] memory) {
        require(limit > 0, "Limit must be greater than 0");
        
        // First, count active products and collect their IDs
        uint256[] memory activeProductIds = new uint256[](allProductIds.length);
        uint256 activeCount = 0;
        
        for (uint256 i = 0; i < allProductIds.length; i++) {
            if (products[allProductIds[i]].isActive) {
                activeProductIds[activeCount] = allProductIds[i];
                activeCount++;
            }
        }
        
        if (offset >= activeCount) {
            return new Product[](0);
        }
        
        uint256 remainingProducts = activeCount - offset;
        uint256 actualLimit = limit > remainingProducts ? remainingProducts : limit;
        
        Product[] memory paginatedProducts = new Product[](actualLimit);
        for (uint256 i = 0; i < actualLimit; i++) {
            paginatedProducts[i] = products[activeProductIds[offset + i]];
        }
        
        return paginatedProducts;
    }

    // MUCH simpler O(1) array operations - no string manipulation!
    function _pushAll(uint256 productId) private {
        allIndex[productId] = allProductIds.length;
        allProductIds.push(productId);
    }
    
    function _removeAll(uint256 productId) private {
        uint256 i = allIndex[productId];
        uint256 last = allProductIds.length - 1;
        if (i != last) {
            uint256 moved = allProductIds[last];
            allProductIds[i] = moved;
            allIndex[moved] = i;
        }
        allProductIds.pop();
        delete allIndex[productId];
    }

    function _pushCat(uint256 categoryId, uint256 productId) private {
        catIndex[categoryId][productId] = categoryProducts[categoryId].length;
        categoryProducts[categoryId].push(productId);
    }
    
    function _removeCat(uint256 categoryId, uint256 productId) private {
        uint256 i = catIndex[categoryId][productId];
        uint256 last = categoryProducts[categoryId].length - 1;
        if (i != last) {
            uint256 moved = categoryProducts[categoryId][last];
            categoryProducts[categoryId][i] = moved;
            catIndex[categoryId][moved] = i;
        }
        categoryProducts[categoryId].pop();
        delete catIndex[categoryId][productId];
    }

    function _pushCreator(address creator, uint256 productId) private {
        creatorIndex[creator][productId] = productsByCreator[creator].length;
        productsByCreator[creator].push(productId);
    }
    
    function _removeCreator(address creator, uint256 productId) private {
        uint256 i = creatorIndex[creator][productId];
        uint256 last = productsByCreator[creator].length - 1;
        if (i != last) {
            uint256 moved = productsByCreator[creator][last];
            productsByCreator[creator][i] = moved;
            creatorIndex[creator][moved] = i;
        }
        productsByCreator[creator].pop();
        delete creatorIndex[creator][productId];
    }

    function _pushAuth(address creator) private {
        authIndex[creator] = authorizedCreatorsList.length;
        authorizedCreatorsList.push(creator);
    }
    
    function _removeAuth(address creator) private {
        uint256 i = authIndex[creator];
        uint256 last = authorizedCreatorsList.length - 1;
        if (i != last) {
            address moved = authorizedCreatorsList[last];
            authorizedCreatorsList[i] = moved;
            authIndex[moved] = i;
        }
        authorizedCreatorsList.pop();
        delete authIndex[creator];
    }
}