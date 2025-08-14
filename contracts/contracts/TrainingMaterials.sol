// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";

contract TrainingMaterials is Ownable {
    struct TrainingMaterial {
        string uuid;
        string title;
        string description;
        uint256 categoryId;
        string imageIPFS;
        string contentIPFS;
        string contextFileIPFS;
        uint256 priceUSDC; // Price in USDC (6 decimals)
        address creator; // Address that created this material
        uint256 createdAt;
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
    mapping(string => TrainingMaterial) public trainingMaterials; // uuid => TrainingMaterial
    mapping(uint256 => string[]) public categoryMaterials; // categoryId => uuid[]
    mapping(address => bool) public authorizedCreators; // Whitelist of addresses that can create materials
    
    uint256 public nextCategoryId;
    uint256 public totalMaterials;
    string[] public allMaterialUuids;
    address[] public authorizedCreatorsList; // Array to track all authorized creators

    // Events
    event CategoryCreated(uint256 indexed categoryId, string name, string description);
    event TrainingMaterialCreated(
        string uuid,
        string title,
        uint256 indexed categoryId,
        string imageIPFS,
        string contentIPFS,
        string contextFileIPFS,
        uint256 priceUSDC,
        address indexed creator
    );
    event CreatorAuthorized(address indexed creator, address indexed authorizedBy);
    event CreatorDeauthorized(address indexed creator, address indexed deauthorizedBy);
    event TrainingMaterialDeleted(string indexed uuid, address indexed deletedBy, address indexed creator);
    event ContractOwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor() Ownable(msg.sender) {
        nextCategoryId = 1;
        totalMaterials = 0;
        
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
        require(authorizedCreators[msg.sender], "Not authorized to create training materials");
        _;
    }

    modifier onlyOwnerOrCreator(string memory uuid) {
        require(trainingMaterials[uuid].exists, "Training material does not exist");
        require(
            msg.sender == owner() || msg.sender == trainingMaterials[uuid].creator,
            "Only owner or creator can delete this material"
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
            totalMaterials
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

    function getAuthorizedCreatorsCount() external view returns (uint256) {
        return authorizedCreatorsList.length;
    }

    // Category management functions (owner only)
    function createCategory(
        string memory _name,
        string memory _description
    ) external onlyOwner returns (uint256) {
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

    // Training material management functions (authorized creators only)
    function createTrainingMaterial(
        string memory _title,
        string memory _description,
        uint256 _categoryId,
        string memory _imageIPFS,
        string memory _contentIPFS,
        string memory _contextFileIPFS,
        uint256 _priceUSDC
    ) external onlyAuthorizedCreator validCategory(_categoryId) returns (string memory) {
        require(bytes(_title).length > 0, "Title cannot be empty");
        require(bytes(_description).length > 0, "Description cannot be empty");
        require(bytes(_imageIPFS).length > 0, "Image IPFS hash cannot be empty");
        require(bytes(_contentIPFS).length > 0, "Content IPFS hash cannot be empty");
        require(bytes(_contextFileIPFS).length > 0, "Context file IPFS hash cannot be empty");

        // Generate UUID based on current block and title
        string memory _uuid = generateUuid(_title);
        require(!trainingMaterials[_uuid].exists, "Generated UUID already exists (very unlikely)");

        trainingMaterials[_uuid] = TrainingMaterial({
            uuid: _uuid,
            title: _title,
            description: _description,
            categoryId: _categoryId,
            imageIPFS: _imageIPFS,
            contentIPFS: _contentIPFS,
            contextFileIPFS: _contextFileIPFS,
            priceUSDC: _priceUSDC,
            creator: msg.sender,
            createdAt: block.timestamp,
            exists: true
        });

        categoryMaterials[_categoryId].push(_uuid);
        allMaterialUuids.push(_uuid);
        totalMaterials++;

        emit TrainingMaterialCreated(_uuid, _title, _categoryId, _imageIPFS, _contentIPFS, _contextFileIPFS, _priceUSDC, msg.sender);
        
        return _uuid;
    }

    // Delete training material (owner or creator only)
    function deleteTrainingMaterial(string memory _uuid) external onlyOwnerOrCreator(_uuid) {
        TrainingMaterial storage material = trainingMaterials[_uuid];
        uint256 categoryId = material.categoryId;
        address creator = material.creator;
        
        // Mark as deleted (set exists to false)
        material.exists = false;
        
        // Remove from category materials array
        string[] storage categoryMats = categoryMaterials[categoryId];
        for (uint256 i = 0; i < categoryMats.length; i++) {
            if (keccak256(abi.encodePacked(categoryMats[i])) == keccak256(abi.encodePacked(_uuid))) {
                // Replace with last element and pop
                categoryMats[i] = categoryMats[categoryMats.length - 1];
                categoryMats.pop();
                break;
            }
        }
        
        // Remove from all materials array
        for (uint256 i = 0; i < allMaterialUuids.length; i++) {
            if (keccak256(abi.encodePacked(allMaterialUuids[i])) == keccak256(abi.encodePacked(_uuid))) {
                // Replace with last element and pop
                allMaterialUuids[i] = allMaterialUuids[allMaterialUuids.length - 1];
                allMaterialUuids.pop();
                break;
            }
        }
        
        // Decrease total count
        totalMaterials--;
        
        emit TrainingMaterialDeleted(_uuid, msg.sender, creator);
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

    function getTrainingMaterial(string memory _uuid) external view returns (TrainingMaterial memory) {
        require(trainingMaterials[_uuid].exists, "Training material does not exist");
        return trainingMaterials[_uuid];
    }

    function getTrainingMaterialsByCategory(uint256 _categoryId) 
        external 
        view 
        validCategory(_categoryId) 
        returns (TrainingMaterial[] memory) 
    {
        string[] memory uuids = categoryMaterials[_categoryId];
        TrainingMaterial[] memory materials = new TrainingMaterial[](uuids.length);
        
        for (uint256 i = 0; i < uuids.length; i++) {
            materials[i] = trainingMaterials[uuids[i]];
        }
        
        return materials;
    }

    function getCategoryMaterialCount(uint256 _categoryId) 
        external 
        view 
        validCategory(_categoryId) 
        returns (uint256) 
    {
        return categoryMaterials[_categoryId].length;
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

    function getAllTrainingMaterials() external view returns (TrainingMaterial[] memory) {
        TrainingMaterial[] memory materials = new TrainingMaterial[](totalMaterials);
        
        for (uint256 i = 0; i < allMaterialUuids.length; i++) {
            materials[i] = trainingMaterials[allMaterialUuids[i]];
        }
        
        return materials;
    }

    function categoryExists(uint256 _categoryId) external view returns (bool) {
        return categories[_categoryId].exists;
    }

    function trainingMaterialExists(string memory _uuid) external view returns (bool) {
        return trainingMaterials[_uuid].exists;
    }

    // Get training materials by creator
    function getTrainingMaterialsByCreator(address _creator) external view returns (TrainingMaterial[] memory) {
        // First count materials by this creator
        uint256 count = 0;
        for (uint256 i = 0; i < allMaterialUuids.length; i++) {
            if (trainingMaterials[allMaterialUuids[i]].creator == _creator) {
                count++;
            }
        }
        
        // Create array with correct size
        TrainingMaterial[] memory materials = new TrainingMaterial[](count);
        uint256 index = 0;
        
        // Fill array with materials by creator
        for (uint256 i = 0; i < allMaterialUuids.length; i++) {
            if (trainingMaterials[allMaterialUuids[i]].creator == _creator) {
                materials[index] = trainingMaterials[allMaterialUuids[i]];
                index++;
            }
        }
        
        return materials;
    }

    function getCreatorMaterialCount(address _creator) external view returns (uint256) {
        uint256 count = 0;
        for (uint256 i = 0; i < allMaterialUuids.length; i++) {
            if (trainingMaterials[allMaterialUuids[i]].creator == _creator) {
                count++;
            }
        }
        return count;
    }
}