// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";

contract TrainingMaterials is Ownable {
    struct TrainingMaterial {
        uint256 id;
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
    mapping(uint256 => TrainingMaterial) public trainingMaterials; // id => TrainingMaterial
    mapping(uint256 => uint256[]) public categoryMaterials; // categoryId => materialId[]
    mapping(address => bool) public authorizedCreators; // Whitelist of addresses that can create materials
    
    uint256 public nextCategoryId;
    uint256 public nextMaterialId;
    uint256[] public allMaterialIds;
    address[] public authorizedCreatorsList; // Array to track all authorized creators

    // Events
    event CategoryCreated(uint256 indexed categoryId, string name, string description);
    event TrainingMaterialCreated(
        uint256 indexed materialId,
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
    event TrainingMaterialDeleted(uint256 indexed materialId, address indexed deletedBy, address indexed creator);
    event ContractOwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor() Ownable(msg.sender) {
        nextCategoryId = 1;
        nextMaterialId = 1;
        
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

    modifier onlyOwnerOrCreator(uint256 materialId) {
        require(trainingMaterials[materialId].exists, "Training material does not exist");
        require(
            msg.sender == owner() || msg.sender == trainingMaterials[materialId].creator,
            "Only owner or creator can delete this material"
        );
        _;
    }

    // State mapping helpers for O(1) array operations
    mapping(uint256 => uint256) private allIndex; // materialId -> index in allMaterialIds
    mapping(uint256 => mapping(uint256 => uint256)) private catIndex; // categoryId, materialId -> index
    
    function _pushAll(uint256 materialId) private {
        allIndex[materialId] = allMaterialIds.length;
        allMaterialIds.push(materialId);
    }
    
    function _removeAll(uint256 materialId) private {
        uint256 i = allIndex[materialId];
        uint256 last = allMaterialIds.length - 1;
        if (i != last) {
            uint256 moved = allMaterialIds[last];
            allMaterialIds[i] = moved;
            allIndex[moved] = i;
        }
        allMaterialIds.pop();
        delete allIndex[materialId];
    }
    
    function _pushCat(uint256 categoryId, uint256 materialId) private {
        catIndex[categoryId][materialId] = categoryMaterials[categoryId].length;
        categoryMaterials[categoryId].push(materialId);
    }
    
    function _removeCat(uint256 categoryId, uint256 materialId) private {
        uint256 i = catIndex[categoryId][materialId];
        uint256 last = categoryMaterials[categoryId].length - 1;
        if (i != last) {
            uint256 moved = categoryMaterials[categoryId][last];
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
    ) external onlyAuthorizedCreator validCategory(_categoryId) returns (uint256) {
        require(bytes(_title).length > 0, "Title cannot be empty");
        require(bytes(_description).length > 0, "Description cannot be empty");
        require(bytes(_imageIPFS).length > 0, "Image IPFS hash cannot be empty");
        require(bytes(_contentIPFS).length > 0, "Content IPFS hash cannot be empty");
        require(bytes(_contextFileIPFS).length > 0, "Context file IPFS hash cannot be empty");

        uint256 materialId = nextMaterialId;
        nextMaterialId++;

        trainingMaterials[materialId] = TrainingMaterial({
            id: materialId,
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

        _pushCat(_categoryId, materialId);
        _pushAll(materialId);

        emit TrainingMaterialCreated(materialId, _title, _categoryId, _imageIPFS, _contentIPFS, _contextFileIPFS, _priceUSDC, msg.sender);
        
        return materialId;
    }

    // Delete training material (owner or creator only)
    function deleteTrainingMaterial(uint256 _materialId) external onlyOwnerOrCreator(_materialId) {
        TrainingMaterial storage material = trainingMaterials[_materialId];
        uint256 categoryId = material.categoryId;
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
    function getCategory(uint256 _categoryId) external view validCategory(_categoryId) returns (Category memory) {
        return categories[_categoryId];
    }

    function getTrainingMaterial(uint256 _materialId) external view returns (TrainingMaterial memory) {
        require(trainingMaterials[_materialId].exists, "Training material does not exist");
        return trainingMaterials[_materialId];
    }

    function getTrainingMaterialsByCategory(uint256 _categoryId) 
        external 
        view 
        validCategory(_categoryId) 
        returns (TrainingMaterial[] memory) 
    {
        uint256[] memory materialIds = categoryMaterials[_categoryId];
        TrainingMaterial[] memory materials = new TrainingMaterial[](materialIds.length);
        
        for (uint256 i = 0; i < materialIds.length; i++) {
            materials[i] = trainingMaterials[materialIds[i]];
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
        TrainingMaterial[] memory materials = new TrainingMaterial[](allMaterialIds.length);
        
        for (uint256 i = 0; i < allMaterialIds.length; i++) {
            materials[i] = trainingMaterials[allMaterialIds[i]];
        }
        
        return materials;
    }

    function categoryExists(uint256 _categoryId) external view returns (bool) {
        return categories[_categoryId].exists;
    }

    function trainingMaterialExists(uint256 _materialId) external view returns (bool) {
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
}