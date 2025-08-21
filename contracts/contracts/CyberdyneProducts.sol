// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";

contract CyberdyneProducts is Ownable {
    struct Product {
        uint64 id;              // Simple incremental ID instead of UUID string
        bytes32 title;
        uint64 categoryId;
        uint256 priceUSDC;       // Price in USDC (6 decimals)
        string metadataURI;      // URI for additional metadata content
        address creator;         // Address that created this product
        uint256 createdAt;
        uint256 updatedAt;
        bool isActive;           // Product availability status
        bool exists;
    }

    struct Category {
        uint64 id;
        bytes32 name;
        string description;
        uint256 createdAt;
        bool exists;
    }

    // Struct for returning categories with string names
    struct CategoryInfo {
        uint64 id;
        string name;
        string description;
        uint256 createdAt;
        bool exists;
    }

    // Struct for returning products with string titles
    struct ProductInfo {
        uint64 id;
        string title;
        uint64 categoryId;
        uint256 priceUSDC;
        string metadataURI;
        address creator;
        uint256 createdAt;
        uint256 updatedAt;
        bool isActive;
        bool exists;
    }

    // Simplified state variables - using uint64 instead of string
    mapping(uint64 => Category) public categories;
    mapping(uint64 => Product) public products;           // id => Product (much simpler!)
    mapping(uint64 => uint64[]) public categoryProducts; // categoryId => productId[]
    mapping(address => uint64[]) public productsByCreator; // creator => productId[]
    mapping(address => bool) public authorizedCreators;
    
    uint64 public nextCategoryId;
    uint64 public nextProductId;                          // Simple counter instead of UUID generation
    uint64[] public allProductIds;                        // uint64[] instead of string[]
    address[] public authorizedCreatorsList;

    // Much simpler index mappings - no nested string mappings!
    mapping(uint64 => uint256) private allIndex;                    // productId -> index in allProductIds
    mapping(uint64 => mapping(uint64 => uint256)) private catIndex; // catId, productId -> index
    mapping(address => mapping(uint64 => uint256)) private creatorIndex; // creator, productId -> index
    mapping(address => uint256) private authIndex;

    // Simplified events
    event CategoryCreated(uint64 indexed categoryId, string name, string description);
    event ProductCreated(
        uint64 indexed productId,  // uint64 instead of string
        string title,
        uint64 indexed categoryId,
        uint256 priceUSDC,
        string metadataURI,
        address indexed creator
    );
    event ProductUpdated(
        uint64 indexed productId,  // uint64 instead of string
        string title,
        uint64 indexed categoryId,
        uint256 priceUSDC,
        string metadataURI,
        address indexed updatedBy
    );
    event ProductStatusChanged(
        uint64 indexed productId,  // uint64 instead of string
        bool isActive,
        address indexed changedBy
    );
    event ProductDeleted(uint64 indexed productId, address indexed deletedBy, address indexed creator);
    event CreatorAuthorized(address indexed creator, address indexed authorizedBy);
    event CreatorDeauthorized(address indexed creator, address indexed deauthorizedBy);

    constructor() Ownable(msg.sender) {
        nextCategoryId = 1;
        nextProductId = 1;       // Start product IDs at 1
        
        // Automatically authorize the contract owner
        authorizedCreators[msg.sender] = true;
        _pushAuth(msg.sender);
    }

    // Helper functions for string <-> bytes32 conversion
    function stringToBytes32(string memory source) internal pure returns (bytes32 result) {
        bytes memory tempEmptyStringTest = bytes(source);
        if (tempEmptyStringTest.length == 0) {
            return 0x0;
        }
        assembly {
            result := mload(add(source, 32))
        }
    }

    function bytes32ToString(bytes32 source) internal pure returns (string memory result) {
        uint8 length = 0;
        while (length < 32 && source[length] != 0) {
            length++;
        }
        assembly {
            result := mload(0x40)
            mstore(0x40, add(result, 0x40))
            mstore(result, length)
            mstore(add(result, 0x20), source)
        }
    }

    // Helper function to convert Product to ProductInfo
    function _productToProductInfo(Product storage product) internal view returns (ProductInfo memory) {
        return ProductInfo({
            id: product.id,
            title: bytes32ToString(product.title),
            categoryId: product.categoryId,
            priceUSDC: product.priceUSDC,
            metadataURI: product.metadataURI,
            creator: product.creator,
            createdAt: product.createdAt,
            updatedAt: product.updatedAt,
            isActive: product.isActive,
            exists: product.exists
        });
    }

    // Simplified modifiers
    modifier validCategory(uint64 categoryId) {
        require(categories[categoryId].exists, "Category does not exist");
        _;
    }

    modifier onlyAuthorizedCreator() {
        require(authorizedCreators[msg.sender], "Not authorized to create products");
        _;
    }

    modifier onlyOwnerOrAuthorizedCreatorOf(uint64 productId) {  // uint64 instead of string
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
    ) external onlyAuthorizedCreator returns (uint64) {
        require(bytes(_name).length > 0, "Category name cannot be empty");
        require(bytes(_name).length <= 32, "Category name too long (max 32 bytes)");
        
        uint64 categoryId = nextCategoryId;
        categories[categoryId] = Category({
            id: categoryId,
            name: stringToBytes32(_name),
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
        uint64 _categoryId,
        uint256 _priceUSDC,
        string memory _metadataURI
    ) external onlyAuthorizedCreator validCategory(_categoryId) returns (uint64) {
        require(bytes(_title).length > 0, "Title cannot be empty");
        require(bytes(_title).length <= 32, "Title too long (max 32 bytes)");
        require(_priceUSDC > 0, "Price must be greater than 0");
        require(bytes(_metadataURI).length > 0, "Metadata URI cannot be empty");

        uint64 productId = nextProductId;  // Simply increment!
        nextProductId++;

        products[productId] = Product({
            id: productId,
            title: stringToBytes32(_title),
            categoryId: _categoryId,
            priceUSDC: _priceUSDC,
            metadataURI: _metadataURI,
            creator: msg.sender,
            createdAt: block.timestamp,
            updatedAt: block.timestamp,
            isActive: true,
            exists: true
        });

        _pushCat(_categoryId, productId);
        _pushCreator(msg.sender, productId);
        _pushAll(productId);

        emit ProductCreated(productId, _title, _categoryId, _priceUSDC, _metadataURI, msg.sender);
        
        return productId;
    }

    // Update product (owner or creator only)
    function updateProduct(
        uint64 _productId,  // uint64 instead of string
        string memory _title,
        uint64 _categoryId,
        uint256 _priceUSDC,
        string memory _metadataURI
    ) external onlyOwnerOrAuthorizedCreatorOf(_productId) validCategory(_categoryId) {
        require(bytes(_title).length > 0, "Title cannot be empty");
        require(bytes(_title).length <= 32, "Title too long (max 32 bytes)");
        require(_priceUSDC > 0, "Price must be greater than 0");
        require(bytes(_metadataURI).length > 0, "Metadata URI cannot be empty");

        Product storage product = products[_productId];
        uint64 oldCategoryId = product.categoryId;
        
        // If category is changing, update category mappings
        if (oldCategoryId != _categoryId) {
            _removeCat(oldCategoryId, _productId);
            _pushCat(_categoryId, _productId);
        }
        
        product.title = stringToBytes32(_title);
        product.categoryId = _categoryId;
        product.priceUSDC = _priceUSDC;
        product.metadataURI = _metadataURI;
        product.updatedAt = block.timestamp;

        emit ProductUpdated(_productId, _title, _categoryId, _priceUSDC, _metadataURI, msg.sender);
    }

    function toggleProductStatus(uint64 _productId) external onlyOwnerOrAuthorizedCreatorOf(_productId) {
        Product storage product = products[_productId];
        product.isActive = !product.isActive;
        product.updatedAt = block.timestamp;

        emit ProductStatusChanged(_productId, product.isActive, msg.sender);
    }

    function deleteProduct(uint64 _productId) external onlyOwnerOrAuthorizedCreatorOf(_productId) {
        Product storage product = products[_productId];
        uint64 categoryId = product.categoryId;
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
    function getCategory(uint64 _categoryId) external view validCategory(_categoryId) returns (Category memory) {
        return categories[_categoryId];
    }

    function getProduct(uint64 _productId) external view returns (Product memory) {
        require(products[_productId].exists, "Product does not exist");
        return products[_productId];
    }

    function getTotalProductCount() external view returns (uint256) {
        return allProductIds.length;
    }

    function productExists(uint64 _productId) external view returns (bool) {
        return products[_productId].exists;
    }

    function categoryExists(uint64 _categoryId) external view returns (bool) {
        return categories[_categoryId].exists;
    }

    // Additional view functions for API compatibility
    function getAllCategories() external view returns (CategoryInfo[] memory) {
        uint256 count = 0;
        for (uint64 i = 1; i < nextCategoryId; i++) {
            if (categories[i].exists) {
                count++;
            }
        }
        
        CategoryInfo[] memory allCategories = new CategoryInfo[](count);
        uint256 index = 0;
        for (uint64 i = 1; i < nextCategoryId; i++) {
            if (categories[i].exists) {
                Category storage cat = categories[i];
                allCategories[index] = CategoryInfo({
                    id: cat.id,
                    name: bytes32ToString(cat.name),
                    description: cat.description,
                    createdAt: cat.createdAt,
                    exists: cat.exists
                });
                index++;
            }
        }
        
        return allCategories;
    }

    function getAllProducts() external view returns (ProductInfo[] memory) {
        ProductInfo[] memory allProducts = new ProductInfo[](allProductIds.length);
        for (uint256 i = 0; i < allProductIds.length; i++) {
            allProducts[i] = _productToProductInfo(products[allProductIds[i]]);
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

    function getAllProductsByCategory(uint64 _categoryId) external view validCategory(_categoryId) returns (ProductInfo[] memory) {
        uint64[] memory categoryProductIds = categoryProducts[_categoryId];
        ProductInfo[] memory categoryProductsArray = new ProductInfo[](categoryProductIds.length);
        
        for (uint256 i = 0; i < categoryProductIds.length; i++) {
            categoryProductsArray[i] = _productToProductInfo(products[categoryProductIds[i]]);
        }
        
        return categoryProductsArray;
    }

    function getAllProductsByCreator(address _creator) external view returns (ProductInfo[] memory) {
        uint64[] memory creatorProductIds = productsByCreator[_creator];
        ProductInfo[] memory creatorProductsArray = new ProductInfo[](creatorProductIds.length);
        
        for (uint256 i = 0; i < creatorProductIds.length; i++) {
            creatorProductsArray[i] = _productToProductInfo(products[creatorProductIds[i]]);
        }
        
        return creatorProductsArray;
    }

    function getCategoryProductCount(uint64 _categoryId) external view validCategory(_categoryId) returns (uint256) {
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
    function getProducts(uint256 offset, uint256 limit) external view returns (ProductInfo[] memory) {
        require(limit > 0, "Limit must be greater than 0");
        
        uint256 totalProducts = allProductIds.length;
        if (offset >= totalProducts) {
            return new ProductInfo[](0);
        }
        
        uint256 remainingProducts = totalProducts - offset;
        uint256 actualLimit = limit > remainingProducts ? remainingProducts : limit;
        
        ProductInfo[] memory paginatedProducts = new ProductInfo[](actualLimit);
        for (uint256 i = 0; i < actualLimit; i++) {
            paginatedProducts[i] = _productToProductInfo(products[allProductIds[offset + i]]);
        }
        
        return paginatedProducts;
    }

    function getProductsByCreator(address creator, uint256 offset, uint256 limit) external view returns (ProductInfo[] memory) {
        require(limit > 0, "Limit must be greater than 0");
        
        uint64[] memory creatorProductIds = productsByCreator[creator];
        uint256 totalProducts = creatorProductIds.length;
        
        if (offset >= totalProducts) {
            return new ProductInfo[](0);
        }
        
        uint256 remainingProducts = totalProducts - offset;
        uint256 actualLimit = limit > remainingProducts ? remainingProducts : limit;
        
        ProductInfo[] memory paginatedProducts = new ProductInfo[](actualLimit);
        for (uint256 i = 0; i < actualLimit; i++) {
            paginatedProducts[i] = _productToProductInfo(products[creatorProductIds[offset + i]]);
        }
        
        return paginatedProducts;
    }

    function getProductsByCategory(uint64 categoryId, uint256 offset, uint256 limit) external view validCategory(categoryId) returns (ProductInfo[] memory) {
        require(limit > 0, "Limit must be greater than 0");
        
        uint64[] memory categoryProductIds = categoryProducts[categoryId];
        uint256 totalProducts = categoryProductIds.length;
        
        if (offset >= totalProducts) {
            return new ProductInfo[](0);
        }
        
        uint256 remainingProducts = totalProducts - offset;
        uint256 actualLimit = limit > remainingProducts ? remainingProducts : limit;
        
        ProductInfo[] memory paginatedProducts = new ProductInfo[](actualLimit);
        for (uint256 i = 0; i < actualLimit; i++) {
            paginatedProducts[i] = _productToProductInfo(products[categoryProductIds[offset + i]]);
        }
        
        return paginatedProducts;
    }

    function getActiveProductsPaginated(uint256 offset, uint256 limit) external view returns (ProductInfo[] memory) {
        require(limit > 0, "Limit must be greater than 0");
        
        // First, count active products and collect their IDs
        uint64[] memory activeProductIds = new uint64[](allProductIds.length);
        uint256 activeCount = 0;
        
        for (uint256 i = 0; i < allProductIds.length; i++) {
            if (products[allProductIds[i]].isActive) {
                activeProductIds[activeCount] = allProductIds[i];
                activeCount++;
            }
        }
        
        if (offset >= activeCount) {
            return new ProductInfo[](0);
        }
        
        uint256 remainingProducts = activeCount - offset;
        uint256 actualLimit = limit > remainingProducts ? remainingProducts : limit;
        
        ProductInfo[] memory paginatedProducts = new ProductInfo[](actualLimit);
        for (uint256 i = 0; i < actualLimit; i++) {
            paginatedProducts[i] = _productToProductInfo(products[activeProductIds[offset + i]]);
        }
        
        return paginatedProducts;
    }

    // MUCH simpler O(1) array operations - no string manipulation!
    function _pushAll(uint64 productId) private {
        allIndex[productId] = allProductIds.length;
        allProductIds.push(productId);
    }
    
    function _removeAll(uint64 productId) private {
        uint256 i = allIndex[productId];
        uint256 last = allProductIds.length - 1;
        if (i != last) {
            uint64 moved = allProductIds[last];
            allProductIds[i] = moved;
            allIndex[moved] = i;
        }
        allProductIds.pop();
        delete allIndex[productId];
    }

    function _pushCat(uint64 categoryId, uint64 productId) private {
        catIndex[categoryId][productId] = categoryProducts[categoryId].length;
        categoryProducts[categoryId].push(productId);
    }
    
    function _removeCat(uint64 categoryId, uint64 productId) private {
        uint256 i = catIndex[categoryId][productId];
        uint256 last = categoryProducts[categoryId].length - 1;
        if (i != last) {
            uint64 moved = categoryProducts[categoryId][last];
            categoryProducts[categoryId][i] = moved;
            catIndex[categoryId][moved] = i;
        }
        categoryProducts[categoryId].pop();
        delete catIndex[categoryId][productId];
    }

    function _pushCreator(address creator, uint64 productId) private {
        creatorIndex[creator][productId] = productsByCreator[creator].length;
        productsByCreator[creator].push(productId);
    }
    
    function _removeCreator(address creator, uint64 productId) private {
        uint256 i = creatorIndex[creator][productId];
        uint256 last = productsByCreator[creator].length - 1;
        if (i != last) {
            uint64 moved = productsByCreator[creator][last];
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

    // Helper functions to get string versions of stored bytes32 data
    function getCategoryName(uint64 _categoryId) external view validCategory(_categoryId) returns (string memory) {
        return bytes32ToString(categories[_categoryId].name);
    }

    function getProductTitle(uint64 _productId) external view returns (string memory) {
        require(products[_productId].exists, "Product does not exist");
        return bytes32ToString(products[_productId].title);
    }
}