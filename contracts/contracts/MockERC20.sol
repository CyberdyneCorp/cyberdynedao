// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MockERC20 is ERC20 {
    uint8 private _decimals;

    constructor(uint256 initialSupply) ERC20("Mock USDC", "USDC") {
        _decimals = 6; // USDC has 6 decimals
        _mint(msg.sender, initialSupply);
    }

    function decimals() public view virtual override returns (uint8) {
        return _decimals;
    }

    // Mint function for testing
    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}