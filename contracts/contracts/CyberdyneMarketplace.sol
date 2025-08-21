// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "./CyberdyneProducts.sol";
import "./CyberdyneAccessNFT.sol";

contract CyberdyneMarketplace is Ownable, ReentrancyGuard {
    using SafeERC20 for IERC20;

    struct Listing {
        uint256 listingId;
        uint64 productId;
        address seller;
        uint256 priceUSDC;
        bool isActive;
        uint256 createdAt;
        uint256 updatedAt;
    }

    struct Sale {
        uint256 saleId;
        uint256 listingId;
        uint64 productId;
        address seller;
        address buyer;
        uint256 priceUSDC;
        uint256 marketplaceFee;
        uint256 sellerAmount;
        uint256 saleTimestamp;
    }

    // State variables
    IERC20 public immutable usdcToken;
    CyberdyneProducts public immutable cyberdyneProducts;
    CyberdyneAccessNFT public immutable accessNFT;

    mapping(uint256 => Listing) public listings;
    mapping(uint64 => uint256) public productToListing; // productId => listingId
    mapping(address => uint256[]) public sellerListings;
    mapping(uint256 => Sale) public sales;
    mapping(address => uint256[]) public buyerSales;
    mapping(address => uint256[]) public sellerSales;

    uint256 public nextListingId;
    uint256 public nextSaleId;
    uint256 public marketplaceFeePercent; // Basis points (e.g., 250 = 2.5%)
    address public feeRecipient;
    bool public marketplaceActive;

    uint256[] public activeListingIds;
    mapping(uint256 => uint256) private listingIndexes; // listingId => index in activeListingIds

    // Events
    event ProductListed(
        uint256 indexed listingId,
        uint64 indexed productId,
        address indexed seller,
        uint256 priceUSDC
    );
    event ProductUnlisted(
        uint256 indexed listingId,
        uint64 indexed productId,
        address indexed seller
    );
    event ProductPriceUpdated(
        uint256 indexed listingId,
        uint64 indexed productId,
        uint256 oldPrice,
        uint256 newPrice
    );
    event ProductSold(
        uint256 indexed saleId,
        uint256 indexed listingId,
        uint64 indexed productId,
        address seller,
        address buyer,
        uint256 priceUSDC,
        uint256 marketplaceFee,
        uint256 sellerAmount
    );
    event MarketplaceFeeUpdated(uint256 oldFee, uint256 newFee);
    event FeeRecipientUpdated(address indexed oldRecipient, address indexed newRecipient);
    event MarketplaceStatusChanged(bool isActive);

    constructor(
        address _usdcToken,
        address _cyberdyneProducts,
        address _accessNFT,
        uint256 _marketplaceFeePercent,
        address _feeRecipient
    ) Ownable(msg.sender) {
        require(_usdcToken != address(0), "Invalid USDC token address");
        require(_cyberdyneProducts != address(0), "Invalid CyberdyneProducts address");
        require(_accessNFT != address(0), "Invalid AccessNFT address");
        require(_feeRecipient != address(0), "Invalid fee recipient address");
        require(_marketplaceFeePercent <= 1000, "Fee cannot exceed 10%"); // Max 10%

        usdcToken = IERC20(_usdcToken);
        cyberdyneProducts = CyberdyneProducts(_cyberdyneProducts);
        accessNFT = CyberdyneAccessNFT(_accessNFT);
        
        marketplaceFeePercent = _marketplaceFeePercent;
        feeRecipient = _feeRecipient;
        marketplaceActive = true;
        
        nextListingId = 1;
        nextSaleId = 1;
    }

    // Modifiers
    modifier onlyActiveSeller() {
        require(marketplaceActive, "Marketplace is not active");
        require(
            accessNFT.addressHasMarketplaceSellAccess(msg.sender) || 
            accessNFT.addressHasAdminAccess(msg.sender) ||
            msg.sender == owner(),
            "Not authorized to sell on marketplace"
        );
        _;
    }

    modifier onlyActiveMarketplace() {
        require(marketplaceActive, "Marketplace is not active");
        _;
    }

    modifier validListing(uint256 listingId) {
        require(listings[listingId].isActive, "Listing does not exist or is inactive");
        _;
    }

    // Listing functions
    function listProduct(uint64 productId) external onlyActiveSeller nonReentrant {
        require(cyberdyneProducts.productExists(productId), "Product does not exist");
        require(productToListing[productId] == 0, "Product already listed");

        // Get product details from the contract
        CyberdyneProducts.Product memory product = cyberdyneProducts.getProduct(productId);
        require(product.isActive, "Product is not active");
        require(
            product.creator == msg.sender || 
            accessNFT.addressHasAdminAccess(msg.sender) ||
            msg.sender == owner(),
            "Only creator, admin, or owner can list this product"
        );

        uint256 listingId = nextListingId++;
        
        listings[listingId] = Listing({
            listingId: listingId,
            productId: productId,
            seller: msg.sender,
            priceUSDC: product.priceUSDC,
            isActive: true,
            createdAt: block.timestamp,
            updatedAt: block.timestamp
        });

        productToListing[productId] = listingId;
        sellerListings[msg.sender].push(listingId);
        
        // Add to active listings
        listingIndexes[listingId] = activeListingIds.length;
        activeListingIds.push(listingId);

        emit ProductListed(listingId, productId, msg.sender, product.priceUSDC);
    }

    function unlistProduct(uint256 listingId) external validListing(listingId) nonReentrant {
        Listing storage listing = listings[listingId];
        require(
            listing.seller == msg.sender || 
            accessNFT.addressHasAdminAccess(msg.sender) ||
            msg.sender == owner(),
            "Only seller, admin, or owner can unlist"
        );

        listing.isActive = false;
        listing.updatedAt = block.timestamp;
        
        // Remove from productToListing mapping
        delete productToListing[listing.productId];
        
        // Remove from active listings
        _removeFromActiveListings(listingId);

        emit ProductUnlisted(listingId, listing.productId, listing.seller);
    }

    function updateListingPrice(uint256 listingId, uint256 newPriceUSDC) external validListing(listingId) nonReentrant {
        Listing storage listing = listings[listingId];
        require(
            listing.seller == msg.sender || 
            accessNFT.addressHasAdminAccess(msg.sender) ||
            msg.sender == owner(),
            "Only seller, admin, or owner can update price"
        );
        require(newPriceUSDC > 0, "Price must be greater than 0");

        uint256 oldPrice = listing.priceUSDC;
        listing.priceUSDC = newPriceUSDC;
        listing.updatedAt = block.timestamp;

        emit ProductPriceUpdated(listingId, listing.productId, oldPrice, newPriceUSDC);
    }

    // Purchase functions
    function purchaseProduct(uint256 listingId) external onlyActiveMarketplace validListing(listingId) nonReentrant {
        Listing storage listing = listings[listingId];
        require(listing.seller != msg.sender, "Cannot buy your own product");

        uint256 totalPrice = listing.priceUSDC;
        uint256 marketplaceFee = (totalPrice * marketplaceFeePercent) / 10000;
        uint256 sellerAmount = totalPrice - marketplaceFee;

        // Check buyer has sufficient USDC balance and allowance
        require(usdcToken.balanceOf(msg.sender) >= totalPrice, "Insufficient USDC balance");
        require(usdcToken.allowance(msg.sender, address(this)) >= totalPrice, "Insufficient USDC allowance");

        // Transfer USDC from buyer
        usdcToken.safeTransferFrom(msg.sender, listing.seller, sellerAmount);
        if (marketplaceFee > 0) {
            usdcToken.safeTransferFrom(msg.sender, feeRecipient, marketplaceFee);
        }

        // Record the sale
        uint256 saleId = nextSaleId++;
        sales[saleId] = Sale({
            saleId: saleId,
            listingId: listingId,
            productId: listing.productId,
            seller: listing.seller,
            buyer: msg.sender,
            priceUSDC: totalPrice,
            marketplaceFee: marketplaceFee,
            sellerAmount: sellerAmount,
            saleTimestamp: block.timestamp
        });

        // Update tracking arrays
        buyerSales[msg.sender].push(saleId);
        sellerSales[listing.seller].push(saleId);

        // Remove listing (product is sold)
        listing.isActive = false;
        listing.updatedAt = block.timestamp;
        delete productToListing[listing.productId];
        _removeFromActiveListings(listingId);

        emit ProductSold(saleId, listingId, listing.productId, listing.seller, msg.sender, totalPrice, marketplaceFee, sellerAmount);
    }

    // Internal helper functions
    function _removeFromActiveListings(uint256 listingId) internal {
        uint256 index = listingIndexes[listingId];
        uint256 lastIndex = activeListingIds.length - 1;
        
        if (index != lastIndex) {
            uint256 lastListingId = activeListingIds[lastIndex];
            activeListingIds[index] = lastListingId;
            listingIndexes[lastListingId] = index;
        }
        
        activeListingIds.pop();
        delete listingIndexes[listingId];
    }

    // View functions
    function getActiveListing(uint256 listingId) external view returns (Listing memory) {
        require(listings[listingId].isActive, "Listing is not active");
        return listings[listingId];
    }

    function getAllActiveListings() external view returns (Listing[] memory) {
        Listing[] memory activeListings = new Listing[](activeListingIds.length);
        
        for (uint256 i = 0; i < activeListingIds.length; i++) {
            activeListings[i] = listings[activeListingIds[i]];
        }
        
        return activeListings;
    }

    function getActiveListingsByCategory(uint64 categoryId) external view returns (Listing[] memory) {
        uint256 count = 0;
        
        // First pass: count matching listings
        for (uint256 i = 0; i < activeListingIds.length; i++) {
            uint256 listingId = activeListingIds[i];
            Listing memory listing = listings[listingId];
            
            CyberdyneProducts.Product memory product = cyberdyneProducts.getProduct(listing.productId);
            if (product.categoryId == categoryId) {
                count++;
            }
        }
        
        // Second pass: populate array
        Listing[] memory categoryListings = new Listing[](count);
        uint256 index = 0;
        
        for (uint256 i = 0; i < activeListingIds.length; i++) {
            uint256 listingId = activeListingIds[i];
            Listing memory listing = listings[listingId];
            
            CyberdyneProducts.Product memory product = cyberdyneProducts.getProduct(listing.productId);
            if (product.categoryId == categoryId) {
                categoryListings[index] = listing;
                index++;
            }
        }
        
        return categoryListings;
    }

    function getSellerListings(address seller) external view returns (Listing[] memory) {
        uint256[] memory sellerListingIds = sellerListings[seller];
        Listing[] memory sellerListingsArray = new Listing[](sellerListingIds.length);
        
        for (uint256 i = 0; i < sellerListingIds.length; i++) {
            sellerListingsArray[i] = listings[sellerListingIds[i]];
        }
        
        return sellerListingsArray;
    }

    function getSale(uint256 saleId) external view returns (Sale memory) {
        require(sales[saleId].saleId != 0, "Sale does not exist");
        return sales[saleId];
    }

    function getBuyerSales(address buyer) external view returns (Sale[] memory) {
        uint256[] memory buyerSaleIds = buyerSales[buyer];
        Sale[] memory buyerSalesArray = new Sale[](buyerSaleIds.length);
        
        for (uint256 i = 0; i < buyerSaleIds.length; i++) {
            buyerSalesArray[i] = sales[buyerSaleIds[i]];
        }
        
        return buyerSalesArray;
    }

    function getSellerSales(address seller) external view returns (Sale[] memory) {
        uint256[] memory sellerSaleIds = sellerSales[seller];
        Sale[] memory sellerSalesArray = new Sale[](sellerSaleIds.length);
        
        for (uint256 i = 0; i < sellerSaleIds.length; i++) {
            sellerSalesArray[i] = sales[sellerSaleIds[i]];
        }
        
        return sellerSalesArray;
    }

    function getActiveListingsCount() external view returns (uint256) {
        return activeListingIds.length;
    }

    function isProductListed(uint64 productId) external view returns (bool) {
        return productToListing[productId] != 0 && listings[productToListing[productId]].isActive;
    }

    function getAllCategories() external view returns (CyberdyneProducts.CategoryInfo[] memory) {
        return cyberdyneProducts.getAllCategories();
    }

    // Admin functions
    function setMarketplaceFee(uint256 _marketplaceFeePercent) external onlyOwner {
        require(_marketplaceFeePercent <= 1000, "Fee cannot exceed 10%");
        
        uint256 oldFee = marketplaceFeePercent;
        marketplaceFeePercent = _marketplaceFeePercent;
        
        emit MarketplaceFeeUpdated(oldFee, _marketplaceFeePercent);
    }

    function setFeeRecipient(address _feeRecipient) external onlyOwner {
        require(_feeRecipient != address(0), "Invalid fee recipient address");
        
        address oldRecipient = feeRecipient;
        feeRecipient = _feeRecipient;
        
        emit FeeRecipientUpdated(oldRecipient, _feeRecipient);
    }

    function setMarketplaceStatus(bool _isActive) external onlyOwner {
        marketplaceActive = _isActive;
        emit MarketplaceStatusChanged(_isActive);
    }

    // Emergency functions
    function emergencyUnlistProduct(uint256 listingId) external onlyOwner {
        require(listings[listingId].isActive, "Listing is not active");
        
        Listing storage listing = listings[listingId];
        listing.isActive = false;
        listing.updatedAt = block.timestamp;
        
        delete productToListing[listing.productId];
        _removeFromActiveListings(listingId);
        
        emit ProductUnlisted(listingId, listing.productId, listing.seller);
    }
}