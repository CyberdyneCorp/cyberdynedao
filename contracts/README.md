# Cyberdyne DAO Smart Contracts

A comprehensive Solidity smart contract system for managing training materials and DAO products with IPFS storage integration.

## Features

### Training Materials Contract
- **Category Management**: Create and manage training material categories
- **Training Materials**: Store training materials with metadata and IPFS links
- **Access Control**: Owner-only functions for creating categories and materials
- **Query Functions**: Retrieve materials by category, get all categories, etc.
- **IPFS Integration**: Store images and content on IPFS with hash references

### Cyberdyne Products Contract
- **Product Management**: Create and manage DAO products
- **Auto-Generated UUIDs**: Unique identifiers for each product
- **Price Management**: USDC pricing with 6-decimal precision
- **IPFS Storage**: Decentralized storage for product content
- **Access Control**: Creator authorization system with owner controls
- **Product Status**: Active/inactive status management
- **Query Functions**: Retrieve products by creator, status, etc.

### Cyberdyne Access NFT Contract
- **ERC721 NFT**: Standard NFT with enumerable extensions for DAO access control
- **Six Access Types**: Learning materials, frontend servers, backend servers, blog creator, admin, marketplace selling
- **Updatable Permissions**: Change access rights after minting (managers only)
- **Manager System**: Authorized addresses can update NFT permissions
- **Batch Operations**: Mint and update multiple NFTs efficiently
- **Custom Metadata**: Individual metadata URIs per token with update capability
- **Address-Based Checking**: Check if user owns tokens with specific access
- **Dynamic Metadata**: On-chain traits with Base64-encoded JSON metadata generation
- **Frontend Integration**: Real-time trait checking with automatic wallet UI updates
- **ERC-4906 Support**: Metadata update events for enhanced frontend compatibility
- **🛡️ Centralized Control**: NFT holders cannot modify their own permissions - only authorized managers can update access rights (this is intentional for maintaining DAO control over access)

## Contract Structure

### TrainingMaterials Contract

#### Data Structures

**TrainingMaterial**
- `uuid`: Auto-generated unique identifier for the material
- `title`: Material title
- `description`: Material description  
- `categoryId`: Associated category ID
- `imageIPFS`: IPFS hash for the material image
- `contentIPFS`: IPFS hash for the material content
- `contextFileIPFS`: IPFS hash for additional context files
- `priceUSDC`: Price in USDC (6 decimal places)
- `creator`: Address of the wallet that created this material
- `createdAt`: Timestamp of creation
- `exists`: Boolean flag for existence check

**Category**
- `id`: Unique category identifier
- `name`: Category name
- `description`: Category description
- `createdAt`: Timestamp of creation
- `exists`: Boolean flag for existence check

#### Owner-Only Functions

- `createCategory(name, description)`: Create a new category
- `authorizeCreator(creator)`: Authorize an address to create training materials
- `deauthorizeCreator(creator)`: Remove authorization from an address (cannot deauthorize owner)
- `transferContractOwnership(newOwner)`: Transfer contract ownership to a new address

#### Authorized Creator Functions

- `createTrainingMaterial(title, description, categoryId, imageIPFS, contentIPFS, contextFileIPFS, priceUSDC)`: Create a new training material (returns auto-generated UUID)

#### Owner or Creator Functions

- `deleteTrainingMaterial(uuid)`: Delete a training material (only owner or original creator can delete)

#### Public View Functions

- `getCategory(categoryId)`: Get category by ID
- `getTrainingMaterial(uuid)`: Get training material by UUID
- `getTrainingMaterialsByCategory(categoryId)`: Get all materials in a category
- `getTrainingMaterialsByCreator(creator)`: Get all materials created by a specific address
- `getAllCategories()`: Get all categories
- `getAllTrainingMaterials()`: Get all training materials (excluding deleted ones)
- `getCategoryMaterialCount(categoryId)`: Get material count for a category
- `getCreatorMaterialCount(creator)`: Get material count for a specific creator
- `getAuthorizedCreators()`: Get list of all authorized creator addresses
- `getAuthorizedCreatorsCount()`: Get count of authorized creators
- `isAuthorizedCreator(creator)`: Check if an address is authorized to create materials
- `categoryExists(categoryId)`: Check if category exists
- `trainingMaterialExists(uuid)`: Check if training material exists (and not deleted)

### CyberdyneProducts Contract

#### Data Structures

**Product**
- `uuid`: Auto-generated unique identifier for the product
- `title`: Product title
- `priceUSDC`: Price in USDC (6 decimal places)
- `ipfsLocation`: IPFS hash for additional product content
- `creator`: Address of the wallet that created this product
- `createdAt`: Timestamp of creation
- `updatedAt`: Timestamp of last update
- `isActive`: Product availability status
- `exists`: Boolean flag for existence check

#### Owner-Only Functions

- `authorizeCreator(creator)`: Authorize an address to create products
- `deauthorizeCreator(creator)`: Remove authorization from an address (cannot deauthorize owner)
- `transferContractOwnership(newOwner)`: Transfer contract ownership to a new address

#### Authorized Creator Functions

- `createProduct(title, priceUSDC, ipfsLocation)`: Create a new product (returns auto-generated UUID)

#### Owner or Creator Functions

- `updateProduct(uuid, title, priceUSDC, ipfsLocation)`: Update an existing product
- `toggleProductStatus(uuid)`: Toggle product active/inactive status
- `deleteProduct(uuid)`: Delete a product (only owner or original creator can delete)

#### Public View Functions

- `getProduct(uuid)`: Get product by UUID
- `getProductsByCreator(creator)`: Get all products created by a specific address
- `getAllProducts()`: Get all products (including inactive ones)
- `getActiveProducts()`: Get only active products
- `productExists(uuid)`: Check if product exists
- `getCreatorProductCount(creator)`: Get product count for a specific creator
- `getActiveProductCount()`: Get count of active products
- `getAuthorizedCreators()`: Get list of all authorized creator addresses
- `isAuthorizedCreator(creator)`: Check if an address is authorized to create products

### CyberdyneAccessNFT Contract

#### Data Structures

**AccessPermissions**
- `learningMaterials`: Boolean access to training materials
- `frontendServers`: Boolean access to frontend development servers
- `backendServers`: Boolean access to backend development servers
- `blogCreator`: Boolean access to create and manage blog content
- `admin`: Boolean administrative access to DAO systems
- `canSellMarketplace`: Boolean permission to sell items on the marketplace
- `issuedAt`: Timestamp when NFT was minted
- `lastUpdated`: Timestamp when permissions were last updated
- `metadataURI`: Custom metadata URI for this specific NFT

#### Owner-Only Functions

- `mint(to, learningMaterials, frontendServers, backendServers, blogCreator, admin, canSellMarketplace, metadataURI)`: Mint new access NFT to address
- `batchMint(recipients[], learningMaterials[], frontendServers[], backendServers[], blogCreator[], admin[], canSellMarketplace[], metadataURIs[])`: Mint multiple NFTs in one transaction
- `authorizeManager(manager)`: Authorize an address to manage NFT permissions
- `deauthorizeManager(manager)`: Remove authorization from an address (cannot deauthorize owner)
- `setBaseURI(baseURI)`: Update the base URI for token metadata
- `transferContractOwnership(newOwner)`: Transfer contract ownership to a new address

#### Manager Functions (Authorized Managers Only)

- `updatePermissions(tokenId, learningMaterials, frontendServers, backendServers, blogCreator, admin, canSellMarketplace)`: Update access permissions for a specific NFT
- `updateMetadata(tokenId, metadataURI)`: Update custom metadata URI for a specific NFT
- `batchUpdatePermissions(tokenIds[], learningMaterials[], frontendServers[], backendServers[], blogCreator[], admin[], canSellMarketplace[])`: Update permissions for multiple NFTs

#### Public View Functions

- `getTokenPermissions(tokenId)`: Get complete permission structure for a token
- `hasLearningAccess(tokenId)`: Check if token has learning materials access
- `hasFrontendAccess(tokenId)`: Check if token has frontend servers access
- `hasBackendAccess(tokenId)`: Check if token has backend servers access
- `hasBlogCreatorAccess(tokenId)`: Check if token has blog creator access
- `hasAdminAccess(tokenId)`: Check if token has admin access
- `hasMarketplaceSellAccess(tokenId)`: Check if token has marketplace selling access
- `hasAccess(tokenId, accessType)`: Check access by string type ("learning", "frontend", "backend", "blogCreator", "admin", "marketplace")
- `addressHasLearningAccess(user)`: Check if user owns any tokens with learning access
- `addressHasFrontendAccess(user)`: Check if user owns any tokens with frontend access
- `addressHasBackendAccess(user)`: Check if user owns any tokens with backend access
- `addressHasBlogCreatorAccess(user)`: Check if user owns any tokens with blog creator access
- `addressHasAdminAccess(user)`: Check if user owns any tokens with admin access
- `addressHasMarketplaceSellAccess(user)`: Check if user owns any tokens with marketplace selling access
- `getUserTokens(user)`: Get all token IDs owned by a user
- `getUserPermissions(user)`: Get all tokens and their permissions for a user
- `getAuthorizedManagers()`: Get list of all authorized managers
- `isAuthorizedManager(manager)`: Check if an address is authorized to manage permissions
- `exists(tokenId)`: Check if a token exists
- `getNextTokenId()`: Get the next token ID that will be minted
- `tokenURI(tokenId)`: Get token metadata URI (supports both custom URIs and dynamic on-chain generation)
- `supportsInterface(interfaceId)`: Check supported interfaces including ERC-4906

## Setup

1. Install dependencies:
```bash
npm install
```

2. Compile contracts:
```bash
npm run compile
```

3. Run tests:
```bash
npm test
```

4. Deploy contracts to local network:
```bash
npx hardhat node

# Deploy TrainingMaterials contract
npm run deploy

# Deploy CyberdyneProducts contract  
npx hardhat run scripts/deploy-products.js --network localhost

# Deploy CyberdyneAccessNFT contract
npx hardhat run scripts/deploy-access-nft.js --network localhost
```

## Testing

### TrainingMaterials Contract Tests
The TrainingMaterials contract includes comprehensive tests covering:
- Contract deployment and initialization
- Creator authorization and deauthorization
- Contract ownership transfer functionality
- Category creation and management (owner-only)
- Training material creation and management (authorized creators)
- Training material deletion (owner or creator only)
- Creator tracking and material ownership
- Price validation and storage (USDC with 6 decimals)
- Access control and authorization checks
- Input validation and error handling
- Query functions (by category, by creator, etc.)
- Data integrity after deletions
- Integration scenarios with multiple creators

### CyberdyneProducts Contract Tests
The CyberdyneProducts contract includes comprehensive tests covering:
- Contract deployment and initialization
- Creator authorization and deauthorization
- Product creation functionality
- Product management (update, toggle status, delete)
- Access control for product operations
- Product querying by creator and status
- Price validation and storage (USDC with 6 decimals)
- IPFS hash validation and storage
- UUID generation and uniqueness
- Data integrity after deletions
- Edge cases and error handling

### CyberdyneAccessNFT Contract Tests
The CyberdyneAccessNFT contract includes comprehensive tests covering:
- Contract deployment and initialization
- Manager authorization and deauthorization
- NFT minting (single and batch operations)
- Permission management and updates
- Access control for permission modifications
- Token-based and address-based access checking
- Custom metadata handling and updates
- Contract ownership transfer functionality
- ERC721Enumerable compliance
- Token transfers and permission persistence
- Edge cases and utility functions

Run tests with:
```bash
npm test
```

## Deployment

Deploy to different networks:

### Local Development
```bash
npx hardhat node  # Start local blockchain
npm run deploy    # Deploy to local network
```

### Base Network Deployment

**Prerequisites:**
1. Create `.env` file from template:
```bash
cp .env.example .env
```

2. Add your private key and BaseScan API key to `.env`:
```bash
PRIVATE_KEY=your_private_key_without_0x_prefix
BASESCAN_API_KEY=your_basescan_api_key_from_basescan.org
```

**Deploy to Base Sepolia Testnet (Recommended for testing):**
```bash
# Deploy TrainingMaterials contract
npm run deploy:base-sepolia

# Deploy CyberdyneProducts contract
npx hardhat run scripts/deploy-products.js --network base-sepolia

# Deploy CyberdyneAccessNFT contract
npx hardhat run scripts/deploy-access-nft.js --network base-sepolia
```

**Deploy to Base Mainnet:**
```bash
# Deploy TrainingMaterials contract
npm run deploy:base-mainnet

# Deploy CyberdyneProducts contract
npx hardhat run scripts/deploy-products.js --network base-mainnet

# Deploy CyberdyneAccessNFT contract
npx hardhat run scripts/deploy-access-nft.js --network base-mainnet
```

**Verify contracts on BaseScan:**
```bash
# After deployment, verify on Sepolia
npm run verify:base-sepolia <CONTRACT_ADDRESS>

# Or verify on mainnet
npm run verify:base-mainnet <CONTRACT_ADDRESS>

# Manual verification with constructor arguments (if needed)
npx hardhat verify --network base-sepolia <CONTRACT_ADDRESS>
npx hardhat verify --network base-mainnet <CONTRACT_ADDRESS>
```

Deployment artifacts are saved to `deployments/` directory.

## Usage Examples

### TrainingMaterials Contract

```javascript
// Only owner can create categories
await trainingContract.createCategory("Blockchain Basics", "Fundamental blockchain concepts");

// Owner can authorize additional creators
await trainingContract.authorizeCreator("0x1234..."); // Address of authorized creator

// Both owner and authorized creators can create materials
const tx = await trainingContract.createTrainingMaterial(
  "Intro to Smart Contracts", 
  "Learn smart contract development",
  1, // category ID
  "QmImageHash...", // IPFS image hash
  "QmContentHash...", // IPFS content hash
  "QmContextHash...", // IPFS context file hash
  ethers.parseUnits("29.99", 6) // 29.99 USDC (6 decimals)
);

// Get the generated UUID and creator from the event
const receipt = await tx.wait();
const event = receipt.logs.find(log => log.eventName === "TrainingMaterialCreated");
const generatedUuid = event.args.uuid;
const creator = event.args.creator;
console.log("Created material with UUID:", generatedUuid, "by:", creator);

// Query materials by category
const materials = await trainingContract.getTrainingMaterialsByCategory(1);

// Query materials by creator
const creatorMaterials = await trainingContract.getTrainingMaterialsByCreator("0x1234...");

// Delete a training material (only owner or creator can delete)
await trainingContract.deleteTrainingMaterial(generatedUuid);
```

### CyberdyneProducts Contract

```javascript
// Owner can authorize additional creators
await productsContract.authorizeCreator("0x1234..."); // Address of authorized creator

// Both owner and authorized creators can create products
const productTx = await productsContract.createProduct(
  "Cyberdyne Product Pro", 
  ethers.parseUnits("99.99", 6), // 99.99 USDC (6 decimals)
  "QmProductContentHash..." // IPFS content hash
);

// Get the generated UUID and creator from the event
const productReceipt = await productTx.wait();
const productEvent = productReceipt.logs.find(log => log.eventName === "ProductCreated");
const productUuid = productEvent.args.uuid;
console.log("Created product with UUID:", productUuid);

// Update product (only owner or creator)
await productsContract.updateProduct(
  productUuid,
  "Cyberdyne Product Pro v2",
  ethers.parseUnits("149.99", 6),
  "QmUpdatedContentHash..."
);

// Toggle product status
await productsContract.toggleProductStatus(productUuid);

// Query products by creator
const creatorProducts = await productsContract.getProductsByCreator("0x1234...");

// Get all active products
const activeProducts = await productsContract.getActiveProducts();

// Delete a product (only owner or creator can delete)
await productsContract.deleteProduct(productUuid);

// Transfer contract ownership to a new address
await productsContract.transferContractOwnership("0x5678..."); // New owner address
```

### CyberdyneAccessNFT Contract

```javascript
// Deploy the NFT contract with name, symbol, and base URI
const CyberdyneAccessNFT = await ethers.getContractFactory("CyberdyneAccessNFT");
const accessNFT = await CyberdyneAccessNFT.deploy(
  "Cyberdyne Access Pass",
  "CYBACC", 
  "https://api.cyberdyne.xyz/metadata/"
);

// Owner can authorize managers to update permissions
await accessNFT.authorizeManager("0x1234..."); // Manager address

// Owner can mint NFTs with specific permissions
const mintTx = await accessNFT.mint(
  "0x5678...", // recipient address
  true,  // learning materials access
  false, // frontend servers access  
  true,  // backend servers access
  false, // blog creator access
  false, // admin access
  true,  // marketplace selling access
  "custom-metadata-uri" // custom metadata URI
);

// Get the token ID from the event
const receipt = await mintTx.wait();
const event = receipt.logs.find(log => log.eventName === "NFTMinted");
const tokenId = event.args.tokenId;

// Authorized managers can update permissions after minting
await accessNFT.connect(manager).updatePermissions(
  tokenId,
  false, // disable learning access
  true,  // enable frontend access
  true,  // keep backend access
  true,  // enable blog creator access
  false, // disable admin access
  false  // disable marketplace selling access
);

// Batch mint multiple NFTs
const recipients = ["0x1111...", "0x2222..."];
const learning = [true, false];
const frontend = [false, true]; 
const backend = [true, false];
const blogCreator = [false, true];
const admin = [false, false];
const canSellMarketplace = [true, false];
const uris = ["uri1", "uri2"];

const tokenIds = await accessNFT.batchMint(recipients, learning, frontend, backend, blogCreator, admin, canSellMarketplace, uris);

// Check individual token permissions
const hasLearning = await accessNFT.hasLearningAccess(tokenId);
const hasFrontend = await accessNFT.hasFrontendAccess(tokenId);
const hasBackend = await accessNFT.hasBackendAccess(tokenId);
const hasBlogCreator = await accessNFT.hasBlogCreatorAccess(tokenId);
const hasAdmin = await accessNFT.hasAdminAccess(tokenId);
const hasMarketplace = await accessNFT.hasMarketplaceSellAccess(tokenId);

// Check if an address has any tokens with specific access
const userHasLearning = await accessNFT.addressHasLearningAccess("0x5678...");
const userHasFrontend = await accessNFT.addressHasFrontendAccess("0x5678...");
const userHasBackend = await accessNFT.addressHasBackendAccess("0x5678...");
const userHasBlogCreator = await accessNFT.addressHasBlogCreatorAccess("0x5678...");
const userHasAdmin = await accessNFT.addressHasAdminAccess("0x5678...");
const userHasMarketplace = await accessNFT.addressHasMarketplaceSellAccess("0x5678...");

// Get all tokens and permissions for a user
const [userTokenIds, permissions] = await accessNFT.getUserPermissions("0x5678...");

// Update custom metadata for a token
await accessNFT.connect(manager).updateMetadata(tokenId, "new-metadata-uri");

// Transfer contract ownership (new owner automatically becomes authorized manager)
await accessNFT.transferContractOwnership("0x9999..."); // New owner address
```

## Security Considerations

- **Access Control**: Only contract owner can create categories and manage creator authorization
- **Creator Whitelist**: Only authorized addresses (including owner) can create training materials
- **Deletion Control**: Only contract owner or original creator can delete training materials
- **Ownership Transfer**: Secure ownership transfer with automatic creator authorization
- **Immutable Creator**: Each material permanently tracks its creator address
- **Owner Protection**: Contract owner cannot be deauthorized from creating materials
- **UUID Uniqueness**: Enforced for training materials using block-based generation
- **Input Validation**: Prevents empty required fields and invalid parameters
- **Data Integrity**: Deleted materials are properly removed from all arrays and counts
- **OpenZeppelin Integration**: Uses battle-tested Ownable contract for access control

### CyberdyneAccessNFT Security
- **🛡️ Centralized Permission Control**: NFT holders cannot modify their own access permissions - only authorized managers can update access rights
- **Manager Authorization**: Only contract owner can authorize/deauthorize permission managers
- **Owner Protection**: Contract owner cannot be deauthorized from managing permissions
- **Access Persistence**: Permissions remain with tokens even after transfers between addresses
- **Batch Security**: All batch operations include proper validation and atomic execution
- **ERC721 Compliance**: Follows OpenZeppelin ERC721 and ERC721Enumerable standards
- **Manager Tracking**: Complete audit trail of who can modify permissions
- **Zero Address Protection**: Prevents operations on invalid addresses
- **Token Existence Validation**: All permission operations validate token existence

## IPFS Integration

The contract stores IPFS hashes for:
- **Images**: Visual representations of training materials
- **Content**: The actual training content (documents, videos, etc.)
- **Context Files**: Additional context files, documentation, or supplementary materials

IPFS provides decentralized storage while the blockchain maintains metadata and references.

## Gas Optimization

- Efficient storage patterns using mappings
- Minimal on-chain data storage (only metadata and IPFS hashes)
- Batched operations for multiple queries
- Event emission for off-chain indexing
- Solidity optimizer enabled (200 runs) - Contract size: ~17.2KB (70% of 24KB limit)

## Network Configuration

The contract is configured for deployment on:
- **Base Mainnet** (Chain ID: 8453)
- **Base Sepolia Testnet** (Chain ID: 84532)
- **Local Hardhat Network** (Chain ID: 1337)

All networks include proper BaseScan integration for contract verification.

## Contract Verification on BaseScan

### Automatic Verification
Hardhat is configured to automatically verify contracts on BaseScan after deployment. The verification uses the `@nomicfoundation/hardhat-verify` plugin.

### Prerequisites for Verification
1. **BaseScan API Key**: Required in your `.env` file
   ```bash
   BASESCAN_API_KEY=your_basescan_api_key_from_basescan.org
   ```

2. **Get BaseScan API Key**:
   - Visit [BaseScan.org](https://basescan.org/apis) for mainnet
   - Visit [Sepolia BaseScan](https://sepolia.basescan.org/apis) for testnet
   - Create an account and generate an API key
   - Add the key to your `.env` file

### Verification Methods

#### Method 1: Automatic Verification During Deployment
The deployment script includes automatic verification. After successful deployment, the contract will be automatically verified on BaseScan.

#### Method 2: Manual Verification After Deployment
```bash
# Verify on Base Sepolia testnet
npx hardhat verify --network base-sepolia <CONTRACT_ADDRESS>

# Verify on Base mainnet
npx hardhat verify --network base-mainnet <CONTRACT_ADDRESS>

# Using npm scripts (same as above but shorter)
npm run verify:base-sepolia <CONTRACT_ADDRESS>
npm run verify:base-mainnet <CONTRACT_ADDRESS>
```

#### Method 3: Verification with Constructor Arguments
If your contract has constructor arguments, include them:
```bash
npx hardhat verify --network base-sepolia <CONTRACT_ADDRESS> "Constructor Arg 1" "Constructor Arg 2"
```

Note: Our TrainingMaterials contract doesn't require constructor arguments.

### Verification Configuration
The `hardhat.config.js` includes proper BaseScan configuration:

```javascript
etherscan: {
  apiKey: {
    "base-mainnet": process.env.BASESCAN_API_KEY || "",
    "base-sepolia": process.env.BASESCAN_API_KEY || ""
  },
  customChains: [
    {
      network: "base-mainnet",
      chainId: 8453,
      urls: {
        apiURL: "https://api.basescan.org/api",
        browserURL: "https://basescan.org"
      }
    },
    {
      network: "base-sepolia", 
      chainId: 84532,
      urls: {
        apiURL: "https://api-sepolia.basescan.org/api",
        browserURL: "https://sepolia.basescan.org"
      }
    }
  ]
}
```

### Verification Troubleshooting

**Common Issues:**

1. **"Contract already verified"**: The contract is already verified on BaseScan
2. **"Invalid API key"**: Check your `BASESCAN_API_KEY` in `.env`
3. **"Compilation error"**: Ensure the same compiler version and settings used for deployment
4. **"Network not supported"**: Verify network name matches `hardhat.config.js`

**Solutions:**
- Ensure your `.env` file has the correct `BASESCAN_API_KEY`
- Wait a few minutes after deployment before attempting verification
- Check that the contract address is correct
- Verify you're using the correct network (base-sepolia vs base-mainnet)

### Verification Benefits
Once verified on BaseScan:
- ✅ Source code is publicly viewable
- ✅ Contract ABI is available for interaction
- ✅ Read/Write functions can be used directly on BaseScan
- ✅ Enhanced transparency and trust
- ✅ Easier integration with frontend applications

### Example Verification Flow
```bash
# 1. Deploy to Base Sepolia
npm run deploy:base-sepolia

# 2. Copy the contract address from deployment output
# 3. Verify the contract (if not auto-verified)
npx hardhat verify --network base-sepolia 0x1234567890abcdef1234567890abcdef12345678

# 4. Visit BaseScan to view verified contract
# https://sepolia.basescan.org/address/0x1234567890abcdef1234567890abcdef12345678
```

## Frontend Integration

### CyberdyneAccessNFT Frontend Features

The frontend automatically integrates with the CyberdyneAccessNFT contract to provide:

- **Real-time Trait Checking**: Automatically checks user's NFT permissions when wallet connects
- **Dynamic UI Updates**: Wallet interface displays active access traits as visual badges
- **Permission-Based Access Control**: Frontend can restrict features based on NFT ownership
- **Metadata Parsing**: Supports both on-chain Base64 metadata and external URI metadata
- **Reactive State Management**: Svelte stores for efficient trait state management

### Frontend Configuration

Add the contract address to your frontend environment:

```bash
# In frontend/.env
VITE_CYBERDYNE_ACCESS_NFT_ADDRESS=0x1234567890abcdef1234567890abcdef12345678
```

### Trait Display Features

- **Learning Materials**: Green badge for educational content access
- **Frontend Servers**: Badge for frontend development server access  
- **Backend Servers**: Badge for backend development server access
- **Blog Creator**: Badge for content creation permissions
- **Admin**: Badge for administrative access
- **Marketplace**: Badge for marketplace selling permissions

### Implementation Details

The frontend integration includes:

1. **CyberdyneAccessNFTManager Class**: TypeScript class for contract interaction
2. **AccessNFT Store**: Svelte store for reactive trait management
3. **Wallet Integration**: Automatic trait checking on wallet connection
4. **UI Components**: Visual trait badges in wallet details panel
5. **Error Handling**: Comprehensive error states and loading indicators

## License

MIT License