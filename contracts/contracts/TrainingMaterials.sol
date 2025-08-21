// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";

contract TrainingMaterials is Ownable {
    struct TrainingMaterial {
        uint64 id;
        bytes32 title;
        uint64 categoryId;
        string metadataURI;
        uint256 priceUSDC; // Price in USDC (6 decimals)
        address creator; // Address that created this material
        uint256 createdAt;
        bool exists;
    }

    struct Category {
        uint64 id;
        bytes32 name;
        string description;
        uint256 createdAt;
        bool exists;
    }

    // State variables
    mapping(uint64 => Category) public categories;
    mapping(uint64 => TrainingMaterial) public trainingMaterials; // id => TrainingMaterial
    mapping(uint64 => uint64[]) public categoryMaterials; // categoryId => materialId[]
    mapping(address => bool) public authorizedCreators; // Whitelist of addresses that can create materials
    
    uint64 public nextCategoryId;
    uint64 public nextMaterialId;
    uint64[] public allMaterialIds;
    address[] public authorizedCreatorsList; // Array to track all authorized creators

    // Events
    event CategoryCreated(uint64 indexed categoryId, string name, string description);
    event TrainingMaterialCreated(
        uint64 indexed materialId,
        string title,
        uint64 indexed categoryId,
        string metadataURI,
        uint256 priceUSDC,
        address indexed creator
    );
    event CreatorAuthorized(address indexed creator, address indexed authorizedBy);
    event CreatorDeauthorized(address indexed creator, address indexed deauthorizedBy);
    event TrainingMaterialDeleted(uint64 indexed materialId, address indexed deletedBy, address indexed creator);
    event ContractOwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor() Ownable(msg.sender) {
        nextCategoryId = 1;
        nextMaterialId = 1;
        
        // Automatically authorize the contract owner
        authorizedCreators[msg.sender] = true;
        authorizedCreatorsList.push(msg.sender);
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

    // Modifiers
    modifier validCategory(uint64 categoryId) {
        require(categories[categoryId].exists, "Category does not exist");
        _;
    }

    modifier onlyAuthorizedCreator() {
        require(authorizedCreators[msg.sender], "Not authorized to create training materials");
        _;
    }

    modifier onlyOwnerOrCreator(uint64 materialId) {
        require(trainingMaterials[materialId].exists, "Training material does not exist");
        require(
            msg.sender == owner() || msg.sender == trainingMaterials[materialId].creator,
            "Only owner or creator can delete this material"
        );
        _;
    }

    // State mapping helpers for O(1) array operations
    mapping(uint64 => uint256) private allIndex; // materialId -> index in allMaterialIds
    mapping(uint64 => mapping(uint64 => uint256)) private catIndex; // categoryId, materialId -> index
    
    function _pushAll(uint64 materialId) private {
        allIndex[materialId] = allMaterialIds.length;
        allMaterialIds.push(materialId);
    }
    
    function _removeAll(uint64 materialId) private {
        uint256 i = allIndex[materialId];
        uint256 last = allMaterialIds.length - 1;
        if (i != last) {
            uint64 moved = allMaterialIds[last];
            allMaterialIds[i] = moved;
            allIndex[moved] = i;
        }
        allMaterialIds.pop();
        delete allIndex[materialId];
    }
    
    function _pushCat(uint64 categoryId, uint64 materialId) private {
        catIndex[categoryId][materialId] = categoryMaterials[categoryId].length;
        categoryMaterials[categoryId].push(materialId);
    }
    
    function _removeCat(uint64 categoryId, uint64 materialId) private {
        uint256 i = catIndex[categoryId][materialId];
        uint256 last = categoryMaterials[categoryId].length - 1;
        if (i != last) {
            uint64 moved = categoryMaterials[categoryId][last];
            categoryMaterials[categoryId][i] = moved;
            catIndex[categoryId][moved] = i;
        }
        categoryMaterials[categoryId].pop();
        delete catIndex[categoryId][materialId];
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
    ) external onlyOwner returns (uint64) {
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

    // Training material management functions (authorized creators only)
    function createTrainingMaterial(
        string memory _title,
        uint64 _categoryId,
        string memory _metadataURI,
        uint256 _priceUSDC
    ) external onlyAuthorizedCreator validCategory(_categoryId) returns (uint64) {
        require(bytes(_title).length > 0, "Title cannot be empty");
        require(bytes(_title).length <= 32, "Title too long (max 32 bytes)");
        require(bytes(_metadataURI).length > 0, "Metadata URI cannot be empty");

        uint64 materialId = nextMaterialId;
        nextMaterialId++;

        trainingMaterials[materialId] = TrainingMaterial({
            id: materialId,
            title: stringToBytes32(_title),
            categoryId: _categoryId,
            metadataURI: _metadataURI,
            priceUSDC: _priceUSDC,
            creator: msg.sender,
            createdAt: block.timestamp,
            exists: true
        });

        _pushCat(_categoryId, materialId);
        _pushAll(materialId);

        emit TrainingMaterialCreated(materialId, _title, _categoryId, _metadataURI, _priceUSDC, msg.sender);
        
        return materialId;
    }

    // Delete training material (owner or creator only)
    function deleteTrainingMaterial(uint64 _materialId) external onlyOwnerOrCreator(_materialId) {
        TrainingMaterial storage material = trainingMaterials[_materialId];
        uint64 categoryId = material.categoryId;
        address creator = material.creator;
        
        // Mark as deleted (set exists to false)
        material.exists = false;
        
        // Remove from arrays using O(1) operations
        _removeCat(categoryId, _materialId);
        _removeAll(_materialId);
        
        emit TrainingMaterialDeleted(_materialId, msg.sender, creator);
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
    function getCategory(uint64 _categoryId) external view validCategory(_categoryId) returns (Category memory) {
        return categories[_categoryId];
    }

    function getTrainingMaterial(uint64 _materialId) external view returns (TrainingMaterial memory) {
        require(trainingMaterials[_materialId].exists, "Training material does not exist");
        return trainingMaterials[_materialId];
    }

    function getTrainingMaterialsByCategory(uint64 _categoryId) 
        external 
        view 
        validCategory(_categoryId) 
        returns (TrainingMaterial[] memory) 
    {
        uint64[] memory materialIds = categoryMaterials[_categoryId];
        TrainingMaterial[] memory materials = new TrainingMaterial[](materialIds.length);
        
        for (uint256 i = 0; i < materialIds.length; i++) {
            materials[i] = trainingMaterials[materialIds[i]];
        }
        
        return materials;
    }

    function getCategoryMaterialCount(uint64 _categoryId) 
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
        
        for (uint64 i = 1; i < nextCategoryId; i++) {
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
        TrainingMaterial[] memory materials = new TrainingMaterial[](allMaterialIds.length);
        
        for (uint256 i = 0; i < allMaterialIds.length; i++) {
            materials[i] = trainingMaterials[allMaterialIds[i]];
        }
        
        return materials;
    }

    function categoryExists(uint64 _categoryId) external view returns (bool) {
        return categories[_categoryId].exists;
    }

    function trainingMaterialExists(uint64 _materialId) external view returns (bool) {
        return trainingMaterials[_materialId].exists;
    }

    // Get training materials by creator
    function getTrainingMaterialsByCreator(address _creator) external view returns (TrainingMaterial[] memory) {
        // First count materials by this creator
        uint256 count = 0;
        for (uint256 i = 0; i < allMaterialIds.length; i++) {
            if (trainingMaterials[allMaterialIds[i]].creator == _creator) {
                count++;
            }
        }
        
        // Create array with correct size
        TrainingMaterial[] memory materials = new TrainingMaterial[](count);
        uint256 index = 0;
        
        // Fill array with materials by creator
        for (uint256 i = 0; i < allMaterialIds.length; i++) {
            if (trainingMaterials[allMaterialIds[i]].creator == _creator) {
                materials[index] = trainingMaterials[allMaterialIds[i]];
                index++;
            }
        }
        
        return materials;
    }

    function getCreatorMaterialCount(address _creator) external view returns (uint256) {
        uint256 count = 0;
        for (uint256 i = 0; i < allMaterialIds.length; i++) {
            if (trainingMaterials[allMaterialIds[i]].creator == _creator) {
                count++;
            }
        }
        return count;
    }
    
    function getTotalMaterialCount() external view returns (uint256) {
        return allMaterialIds.length;
    }

    // Helper functions to get string versions of stored bytes32 data
    function getCategoryName(uint64 _categoryId) external view validCategory(_categoryId) returns (string memory) {
        return bytes32ToString(categories[_categoryId].name);
    }

    function getTrainingMaterialTitle(uint64 _materialId) external view returns (string memory) {
        require(trainingMaterials[_materialId].exists, "Training material does not exist");
        return bytes32ToString(trainingMaterials[_materialId].title);
    }
}