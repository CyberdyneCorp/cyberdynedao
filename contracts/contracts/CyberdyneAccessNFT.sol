// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/Pausable.sol";

contract CyberdyneAccessNFT is ERC721, ERC721Enumerable, Ownable, Pausable {
    using Strings for uint256;

    enum AccessType {
        LEARNING,
        FRONTEND,
        BACKEND,
        BLOG_CREATOR,
        ADMIN,
        MARKETPLACE
    }

    struct AccessPermissions {
        bool learningMaterials;    // Access to training materials
        bool frontendServers;      // Access to frontend development servers
        bool backendServers;       // Access to backend development servers
        bool blogCreator;          // Access to create and manage blog content
        bool admin;                // Administrative access to DAO systems
        bool canSellMarketplace;   // Permission to sell items on the marketplace
        uint256 issuedAt;          // Timestamp when NFT was minted
        uint256 lastUpdated;       // Timestamp when permissions were last updated
        string metadataURI;        // Custom metadata URI for this NFT
    }

    // State variables
    mapping(uint256 => AccessPermissions) public tokenPermissions;
    mapping(address => bool) public authorizedManagers; // Addresses that can update permissions
    
    uint256 private _nextTokenId;
    string private _baseTokenURI;
    address[] public authorizedManagersList;

    // Events
    event NFTMinted(
        uint256 indexed tokenId,
        address indexed to,
        bool learningMaterials,
        bool frontendServers,
        bool backendServers,
        bool blogCreator,
        bool admin,
        bool canSellMarketplace
    );
    event PermissionsUpdated(
        uint256 indexed tokenId,
        bool learningMaterials,
        bool frontendServers,
        bool backendServers,
        bool blogCreator,
        bool admin,
        bool canSellMarketplace,
        address indexed updatedBy
    );
    event MetadataUpdated(
        uint256 indexed tokenId,
        string metadataURI,
        address indexed updatedBy
    );
    event ManagerAuthorized(address indexed manager, address indexed authorizedBy);
    event ManagerDeauthorized(address indexed manager, address indexed deauthorizedBy);

    constructor(
        string memory name,
        string memory symbol,
        string memory baseURI
    ) ERC721(name, symbol) Ownable(msg.sender) {
        _baseTokenURI = baseURI;
        _nextTokenId = 1;
        
        // Automatically authorize the contract owner as manager
        authorizedManagers[msg.sender] = true;
        authorizedManagersList.push(msg.sender);
    }

    // Modifiers
    modifier onlyAuthorizedManager() {
        require(authorizedManagers[msg.sender] || msg.sender == owner(), "Not authorized to manage permissions");
        _;
    }

    modifier tokenExists(uint256 tokenId) {
        require(_ownerOf(tokenId) != address(0), "Token does not exist");
        _;
    }

    // Manager authorization functions (owner only)
    function authorizeManager(address _manager) external onlyOwner {
        require(_manager != address(0), "Cannot authorize zero address");
        require(!authorizedManagers[_manager], "Manager already authorized");
        
        authorizedManagers[_manager] = true;
        authorizedManagersList.push(_manager);
        
        emit ManagerAuthorized(_manager, msg.sender);
    }

    function deauthorizeManager(address _manager) external onlyOwner {
        require(_manager != address(0), "Cannot deauthorize zero address");
        require(authorizedManagers[_manager], "Manager not authorized");
        require(_manager != owner(), "Cannot deauthorize contract owner");
        
        authorizedManagers[_manager] = false;
        
        // Remove from array (find and replace with last element)
        for (uint256 i = 0; i < authorizedManagersList.length; i++) {
            if (authorizedManagersList[i] == _manager) {
                authorizedManagersList[i] = authorizedManagersList[authorizedManagersList.length - 1];
                authorizedManagersList.pop();
                break;
            }
        }
        
        emit ManagerDeauthorized(_manager, msg.sender);
    }

    function isAuthorizedManager(address _manager) external view returns (bool) {
        return authorizedManagers[_manager] || _manager == owner();
    }

    function getAuthorizedManagers() external view returns (address[] memory) {
        return authorizedManagersList;
    }

    // Minting functions
    function mint(
        address to,
        bool learningMaterials,
        bool frontendServers,
        bool backendServers,
        bool blogCreator,
        bool admin,
        bool canSellMarketplace,
        string memory metadataURI
    ) external onlyOwner whenNotPaused returns (uint256) {
        require(to != address(0), "Cannot mint to zero address");
        
        uint256 tokenId = _nextTokenId;
        _nextTokenId++;
        
        _safeMint(to, tokenId);
        
        tokenPermissions[tokenId] = AccessPermissions({
            learningMaterials: learningMaterials,
            frontendServers: frontendServers,
            backendServers: backendServers,
            blogCreator: blogCreator,
            admin: admin,
            canSellMarketplace: canSellMarketplace,
            issuedAt: block.timestamp,
            lastUpdated: block.timestamp,
            metadataURI: metadataURI
        });
        
        emit NFTMinted(tokenId, to, learningMaterials, frontendServers, backendServers, blogCreator, admin, canSellMarketplace);
        
        return tokenId;
    }

    function batchMint(
        address[] memory recipients,
        bool[] memory learningMaterials,
        bool[] memory frontendServers,
        bool[] memory backendServers,
        bool[] memory blogCreator,
        bool[] memory admin,
        bool[] memory canSellMarketplace,
        string[] memory metadataURIs
    ) external onlyOwner whenNotPaused returns (uint256[] memory) {
        require(recipients.length > 0, "No recipients provided");
        require(
            recipients.length == learningMaterials.length &&
            recipients.length == frontendServers.length &&
            recipients.length == backendServers.length &&
            recipients.length == blogCreator.length &&
            recipients.length == admin.length &&
            recipients.length == canSellMarketplace.length &&
            recipients.length == metadataURIs.length,
            "Array lengths must match"
        );
        
        uint256[] memory tokenIds = new uint256[](recipients.length);
        
        for (uint256 i = 0; i < recipients.length; i++) {
            require(recipients[i] != address(0), "Cannot mint to zero address");
            
            uint256 tokenId = _nextTokenId;
            _nextTokenId++;
            
            _safeMint(recipients[i], tokenId);
            
            tokenPermissions[tokenId] = AccessPermissions({
                learningMaterials: learningMaterials[i],
                frontendServers: frontendServers[i],
                backendServers: backendServers[i],
                blogCreator: blogCreator[i],
                admin: admin[i],
                canSellMarketplace: canSellMarketplace[i],
                issuedAt: block.timestamp,
                lastUpdated: block.timestamp,
                metadataURI: metadataURIs[i]
            });
            
            emit NFTMinted(tokenId, recipients[i], learningMaterials[i], frontendServers[i], backendServers[i], blogCreator[i], admin[i], canSellMarketplace[i]);
            tokenIds[i] = tokenId;
        }
        
        return tokenIds;
    }

    // Permission management functions
    function updatePermissions(
        uint256 tokenId,
        bool learningMaterials,
        bool frontendServers,
        bool backendServers,
        bool blogCreator,
        bool admin,
        bool canSellMarketplace
    ) external onlyAuthorizedManager tokenExists(tokenId) whenNotPaused {
        AccessPermissions storage permissions = tokenPermissions[tokenId];
        
        permissions.learningMaterials = learningMaterials;
        permissions.frontendServers = frontendServers;
        permissions.backendServers = backendServers;
        permissions.blogCreator = blogCreator;
        permissions.admin = admin;
        permissions.canSellMarketplace = canSellMarketplace;
        permissions.lastUpdated = block.timestamp;
        
        emit PermissionsUpdated(tokenId, learningMaterials, frontendServers, backendServers, blogCreator, admin, canSellMarketplace, msg.sender);
    }

    function updateMetadata(
        uint256 tokenId,
        string memory metadataURI
    ) external onlyAuthorizedManager tokenExists(tokenId) whenNotPaused {
        tokenPermissions[tokenId].metadataURI = metadataURI;
        tokenPermissions[tokenId].lastUpdated = block.timestamp;
        
        emit MetadataUpdated(tokenId, metadataURI, msg.sender);
    }

    function batchUpdatePermissions(
        uint256[] memory tokenIds,
        bool[] memory learningMaterials,
        bool[] memory frontendServers,
        bool[] memory backendServers,
        bool[] memory blogCreator,
        bool[] memory admin,
        bool[] memory canSellMarketplace
    ) external onlyAuthorizedManager whenNotPaused {
        require(tokenIds.length > 0, "No token IDs provided");
        require(
            tokenIds.length == learningMaterials.length &&
            tokenIds.length == frontendServers.length &&
            tokenIds.length == backendServers.length &&
            tokenIds.length == blogCreator.length &&
            tokenIds.length == admin.length &&
            tokenIds.length == canSellMarketplace.length,
            "Array lengths must match"
        );
        
        for (uint256 i = 0; i < tokenIds.length; i++) {
            require(_ownerOf(tokenIds[i]) != address(0), "Token does not exist");
            
            AccessPermissions storage permissions = tokenPermissions[tokenIds[i]];
            
            permissions.learningMaterials = learningMaterials[i];
            permissions.frontendServers = frontendServers[i];
            permissions.backendServers = backendServers[i];
            permissions.blogCreator = blogCreator[i];
            permissions.admin = admin[i];
            permissions.canSellMarketplace = canSellMarketplace[i];
            permissions.lastUpdated = block.timestamp;
            
            emit PermissionsUpdated(tokenIds[i], learningMaterials[i], frontendServers[i], backendServers[i], blogCreator[i], admin[i], canSellMarketplace[i], msg.sender);
        }
    }

    // Access check functions
    function hasLearningAccess(uint256 tokenId) external view tokenExists(tokenId) returns (bool) {
        return tokenPermissions[tokenId].learningMaterials;
    }

    function hasFrontendAccess(uint256 tokenId) external view tokenExists(tokenId) returns (bool) {
        return tokenPermissions[tokenId].frontendServers;
    }

    function hasBackendAccess(uint256 tokenId) external view tokenExists(tokenId) returns (bool) {
        return tokenPermissions[tokenId].backendServers;
    }

    function hasBlogCreatorAccess(uint256 tokenId) external view tokenExists(tokenId) returns (bool) {
        return tokenPermissions[tokenId].blogCreator;
    }

    function hasAdminAccess(uint256 tokenId) external view tokenExists(tokenId) returns (bool) {
        return tokenPermissions[tokenId].admin;
    }

    function hasMarketplaceSellAccess(uint256 tokenId) external view tokenExists(tokenId) returns (bool) {
        return tokenPermissions[tokenId].canSellMarketplace;
    }

    function hasAccess(uint256 tokenId, AccessType accessType) external view tokenExists(tokenId) returns (bool) {
        AccessPermissions memory permissions = tokenPermissions[tokenId];
        
        if (accessType == AccessType.LEARNING) {
            return permissions.learningMaterials;
        } else if (accessType == AccessType.FRONTEND) {
            return permissions.frontendServers;
        } else if (accessType == AccessType.BACKEND) {
            return permissions.backendServers;
        } else if (accessType == AccessType.BLOG_CREATOR) {
            return permissions.blogCreator;
        } else if (accessType == AccessType.ADMIN) {
            return permissions.admin;
        } else if (accessType == AccessType.MARKETPLACE) {
            return permissions.canSellMarketplace;
        }
        
        return false;
    }

    // Helper function to check if an address has access (checks all tokens owned)
    function addressHasLearningAccess(address user) external view returns (bool) {
        uint256 balance = balanceOf(user);
        for (uint256 i = 0; i < balance; i++) {
            uint256 tokenId = tokenOfOwnerByIndex(user, i);
            if (tokenPermissions[tokenId].learningMaterials) {
                return true;
            }
        }
        return false;
    }

    function addressHasFrontendAccess(address user) external view returns (bool) {
        uint256 balance = balanceOf(user);
        for (uint256 i = 0; i < balance; i++) {
            uint256 tokenId = tokenOfOwnerByIndex(user, i);
            if (tokenPermissions[tokenId].frontendServers) {
                return true;
            }
        }
        return false;
    }

    function addressHasBackendAccess(address user) external view returns (bool) {
        uint256 balance = balanceOf(user);
        for (uint256 i = 0; i < balance; i++) {
            uint256 tokenId = tokenOfOwnerByIndex(user, i);
            if (tokenPermissions[tokenId].backendServers) {
                return true;
            }
        }
        return false;
    }

    function addressHasBlogCreatorAccess(address user) external view returns (bool) {
        uint256 balance = balanceOf(user);
        for (uint256 i = 0; i < balance; i++) {
            uint256 tokenId = tokenOfOwnerByIndex(user, i);
            if (tokenPermissions[tokenId].blogCreator) {
                return true;
            }
        }
        return false;
    }

    function addressHasAdminAccess(address user) external view returns (bool) {
        uint256 balance = balanceOf(user);
        for (uint256 i = 0; i < balance; i++) {
            uint256 tokenId = tokenOfOwnerByIndex(user, i);
            if (tokenPermissions[tokenId].admin) {
                return true;
            }
        }
        return false;
    }

    function addressHasMarketplaceSellAccess(address user) external view returns (bool) {
        uint256 balance = balanceOf(user);
        for (uint256 i = 0; i < balance; i++) {
            uint256 tokenId = tokenOfOwnerByIndex(user, i);
            if (tokenPermissions[tokenId].canSellMarketplace) {
                return true;
            }
        }
        return false;
    }

    // Get functions
    function getTokenPermissions(uint256 tokenId) 
        external 
        view 
        tokenExists(tokenId) 
        returns (AccessPermissions memory) 
    {
        return tokenPermissions[tokenId];
    }

    function getUserTokens(address user) external view returns (uint256[] memory) {
        uint256 balance = balanceOf(user);
        uint256[] memory tokens = new uint256[](balance);
        
        for (uint256 i = 0; i < balance; i++) {
            tokens[i] = tokenOfOwnerByIndex(user, i);
        }
        
        return tokens;
    }

    function getUserPermissions(address user) 
        external 
        view 
        returns (uint256[] memory tokenIds, AccessPermissions[] memory permissions) 
    {
        uint256 balance = balanceOf(user);
        tokenIds = new uint256[](balance);
        permissions = new AccessPermissions[](balance);
        
        for (uint256 i = 0; i < balance; i++) {
            uint256 tokenId = tokenOfOwnerByIndex(user, i);
            tokenIds[i] = tokenId;
            permissions[i] = tokenPermissions[tokenId];
        }
        
        return (tokenIds, permissions);
    }

    // Token URI functions
    function tokenURI(uint256 tokenId) 
        public 
        view 
        override 
        tokenExists(tokenId) 
        returns (string memory) 
    {
        string memory customURI = tokenPermissions[tokenId].metadataURI;
        
        if (bytes(customURI).length > 0) {
            return customURI;
        }
        
        string memory baseURI = _baseURI();
        return bytes(baseURI).length > 0 
            ? string(abi.encodePacked(baseURI, tokenId.toString()))
            : "";
    }

    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }

    function setBaseURI(string memory baseURI) external onlyOwner {
        _baseTokenURI = baseURI;
    }

    // Transfer contract ownership and ensure new owner is authorized
    function transferContractOwnership(address _newOwner) external onlyOwner {
        require(_newOwner != address(0), "New owner cannot be zero address");
        require(_newOwner != owner(), "New owner cannot be the same as current owner");
        
        // Authorize new owner if not already authorized
        if (!authorizedManagers[_newOwner]) {
            authorizedManagers[_newOwner] = true;
            authorizedManagersList.push(_newOwner);
        }
        
        // Transfer ownership using OpenZeppelin's function
        _transferOwnership(_newOwner);
    }

    // Required overrides for ERC721Enumerable
    function _update(address to, uint256 tokenId, address auth)
        internal
        override(ERC721, ERC721Enumerable)
        whenNotPaused
        returns (address)
    {
        return super._update(to, tokenId, auth);
    }

    function _increaseBalance(address account, uint128 value)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._increaseBalance(account, value);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    // Utility functions
    function totalSupply() public view override returns (uint256) {
        return _nextTokenId - 1;
    }

    function exists(uint256 tokenId) external view returns (bool) {
        return _ownerOf(tokenId) != address(0);
    }

    function getNextTokenId() external view returns (uint256) {
        return _nextTokenId;
    }

    // Pause functions
    function pause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }
}