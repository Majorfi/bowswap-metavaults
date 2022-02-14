// SPDX-License-Identifier: MIT

pragma solidity ^0.8.10;
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/proxy/utils/Initializable.sol";

interface Vault is IERC20 {
    function decimals() external view returns (uint256);

    function deposit() external returns (uint256);

    function deposit(uint256 amount) external returns (uint256);

    function deposit(uint256 amount, address recipient)
        external
        returns (uint256);

    function withdraw() external returns (uint256);

    function withdraw(uint256 maxShares) external returns (uint256);

    function withdraw(uint256 maxShares, address recipient)
        external
        returns (uint256);

    function token() external view returns (address);

    function pricePerShare() external view returns (uint256);

    function totalAssets() external view returns (uint256);

    function permit(
        address owner,
        address spender,
        uint256 amount,
        uint256 expiry,
        bytes calldata signature
    ) external returns (bool);
}

interface Bowswap {
    enum Action {Deposit, Withdraw, Swap}
    struct Swap {
        Action action;
        address pool;
        uint128 n;
        uint128 m;
    }
    function swap(address from_vault, address to_vault, uint256 amount, uint256 min_amount_out, Swap[] calldata instructions, uint256 donation, uint256 origin) external;
    function estimate_out(address from_vault, address to_vault, uint256 amount, Swap[] calldata instructions, uint256 donation) external view returns (uint256);
}

interface   YearnRegistry {
    function latestVault(address) external view returns (address);
}

contract MetaVault {
    YearnRegistry public constant yRegistry = YearnRegistry(0x50c1a2eA0a861A967D9d0FFE2AE4012c2E053804);
    Bowswap public bowswap = Bowswap(0xaF0CB47a1bB9115DCA563BcC7C2EAbD711cCa685);
    Vault public currentVault;
    uint256 public currentDecimals;
    uint256 public power = 1e18;
    uint256 public totalShares;
    mapping(address => uint256) public shares;
    mapping(address => mapping(address => uint256)) public balanceOfIn;

    string constant public name = "MetaVault curveEURS + curveEURT + curveibEUR + curveEURN + curve3EUR";

    constructor(address _token, address _bowswap) {
        currentVault = Vault(yRegistry.latestVault(_token));
        currentDecimals = currentVault.decimals();
        bowswap = Bowswap(_bowswap);
    }


    /**
        @notice Retrieve, for a given _owner, the number of shares it owns in this metavault
        @param _owner Address for which we want the number of shares
        @return Shares in WEI
    */
    function getShares(address _owner) public view returns (uint256) {
        return shares[_owner] * power / 1e18;
    }

    /**
        @notice Helper function to retrieve the total number of shares for
        the whole metavault. Match the balanceOf this in the currentVault.
        @return balanceOf this in currentVault
    */
    function metaVaultTotalShare() public view returns (uint256) {
        return currentVault.balanceOf(address(this));
    }

    /**
        @notice Helper function to retrieve the currentVault pricePerShare.
        @return Price per share of the currentVault
    */
    function underlyingPricePerShare() public view returns (uint256) {
        return currentVault.pricePerShare();
    }

	function	deposit(uint256 _amountToDeposit, address _recipient) public returns (uint256) {
		IERC20 _currentVaultWant = IERC20(currentVault.token());
		uint256 _depositorBalance = _currentVaultWant.balanceOf(msg.sender);
		if (_depositorBalance < _amountToDeposit) {
			_amountToDeposit = _depositorBalance;
		}
		_currentVaultWant.transferFrom(msg.sender, address(this), _amountToDeposit);

        _currentVaultWant.approve(address(currentVault), _amountToDeposit);
		uint256 _shareForDepositor = currentVault.deposit(_amountToDeposit);

		shares[_recipient] += _shareForDepositor;
        totalShares = totalShares + _shareForDepositor;
		return _shareForDepositor;
	}

    function    withdraw(uint256 _shareToRedeem, address _recipient) public returns (uint256) {
        require(shares[msg.sender] > 0, "No shares");

        uint256 share = shares[msg.sender];
        if (share > _shareToRedeem) {
            share = _shareToRedeem;
        }
        shares[msg.sender] -= share;
        totalShares -= share;
        uint256 redeemedValue = currentVault.withdraw(share, _recipient);
        return redeemedValue;
    }

    function    estimateMigration(address _token, Bowswap.Swap[] calldata _instructions) public view returns (uint256) {
        return bowswap.estimate_out(
            address(currentVault),
            yRegistry.latestVault(_token),
            metaVaultTotalShare(),
            _instructions,
            30
        );
    }
    function    swap(address _token, uint256 _minAmountOut, Bowswap.Swap[] calldata _instructions) public {
        address toVault = yRegistry.latestVault(_token);
        uint256 previousTotalShare = metaVaultTotalShare();
        uint256 previousDecimals = 10 ** currentDecimals;

        currentVault.approve(address(bowswap), metaVaultTotalShare());
        bowswap.swap(address(currentVault), toVault, metaVaultTotalShare(), _minAmountOut, _instructions, 30, 1);
        currentVault = Vault(toVault);
        currentDecimals = currentVault.decimals();

        uint256 newTotalShare = metaVaultTotalShare();
        uint256 newDecimals = (10 ** currentDecimals);
        uint256 evolution = 0;
        if (newDecimals < previousDecimals) {
            uint256 previousScaledTotalShares = previousTotalShare * newDecimals / previousDecimals;
            evolution = newTotalShare * previousDecimals / previousScaledTotalShares;
        } else {
            evolution = newTotalShare * previousDecimals / previousTotalShare;
        }
        power = power * evolution / 1e18;
    }
}