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
```

**Deploy to Base Mainnet:**
```bash
# Deploy TrainingMaterials contract
npm run deploy:base-mainnet

# Deploy CyberdyneProducts contract
npx hardhat run scripts/deploy-products.js --network base-mainnet
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

## License

MIT License