import time
import pytest
from brownie import MetaVault, VaultSwapperFtm, Contract, Wei, accounts, chain, convert

RARITY_EXTENDED_GOLD = '0x2069B76Afe6b734Fb65D1d099E7ec64ee9CC76B2'
RARITY_EXTENDED_COOKING = '0x7474002fe5640d612c9a76cb0b6857932ff891e8'
RARITY_EXTENDED_COOKING_HELPER = '0xFE23ea8C57Ee4f28E9C60cA09C512Ce80e90E6F5'

VAULT_DAI = '0x637eC617c86D24E421328e6CAEa1d92114892439'
TOKEN_DAI = '0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E'
WHALE_DAI = '0xd8c8edf5e23a4f69aee60747294482e941dcbea0'
BIG_WHALE_DAI = '0x8d9aed9882b4953a0c9fa920168fa1fdfa0ebe75'

VAULT_USDC = '0xEF0210eB96c7EB36AF8ed1c20306462764935607'
TOKEN_USDC = '0x04068DA6C83AFCFA0e13ba15A6696662335D5B75'
BIG_WHALE_USDC = '0x328a7b4d538a2b3942653a9983fda3c12c571141'

VAULT_MIM = '0x0A0b23D9786963DE69CB2447dC125c49929419d8'
TOKEN_MIM = '0x82f0B8B456c1A451378467398982d4834b6829c1'

chain.reset()
deployer = accounts[0]
depositor = accounts[1]
another_depositor = accounts[2]
bowswap = deployer.deploy(VaultSwapperFtm)
bowswap.initialize(deployer, {"from": deployer})
metaVault = deployer.deploy(MetaVault, VAULT_DAI, bowswap)
dai = Contract.from_explorer(TOKEN_DAI)
usdc = Contract.from_explorer(TOKEN_USDC)

def simulate_harvest(token, whale, vault):
	print('SIMULATING HARVEST WITH 100_000_000 USDC EARNED')
	token.transfer(vault, 100000000e6, {'from': whale})

def print_situation(shareUnit):
	vaultPPS = float('{0:.2f}'.format(metaVault.underlyingPricePerShare().to(shareUnit)))
	depositorShare = float('{0:.2f}'.format(metaVault.getShares(depositor).to('ether')))
	anotherDepositorShare = float('{0:.2f}'.format(metaVault.getShares(another_depositor).to('ether')))
	print('--------------------------------')
	print('TotalShare: ' + convert.to_string(metaVault.metaVaultTotalShare().to(shareUnit)))
	print('Underlying PPS: ' + convert.to_string(metaVault.underlyingPricePerShare().to(shareUnit)))
	print('Depositor Share: ' + convert.to_string(metaVault.getShares(depositor).to('ether')) + ' (' + str(round(vaultPPS * depositorShare)) + '$)')
	print('Another Depositor Share: ' + convert.to_string(metaVault.getShares(another_depositor).to('ether')) + ' (' + str(round(vaultPPS * anotherDepositorShare)) + '$)')
	print('--------------------------------')

def init_metavault():
	assert metaVault.metaVaultTotalShare() == 0
	assert metaVault.getShares(depositor) == 0

	# Take some DAI from the whales to work with
	dai.transfer(depositor, 1000e18, {'from': WHALE_DAI})
	assert dai.balanceOf(depositor) >= 1000e18
	dai.transfer(another_depositor, 500e18, {'from': WHALE_DAI})
	assert dai.balanceOf(another_depositor) >= 500e18

	# Deposit some DAI from depositor
	dai.approve(metaVault.address, 1000e18, {'from': depositor})
	assert dai.allowance(depositor, metaVault.address) == 1000e18
	metaVault.deposit(1000e18, depositor, {'from': depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 1000e18, abs=1e18)

	print_situation('ether')

	# Deposit some DAI from another_depositor
	dai.approve(metaVault.address, 500e18, {'from': another_depositor})
	assert dai.allowance(another_depositor, metaVault.address) == 500e18
	metaVault.deposit(500e18, another_depositor, {'from': another_depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1500e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 500e18, abs=1e18)

	# Withdraw some DAI from depositor
	metaVault.withdraw(500e18, depositor, {'from': depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 500e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 500e18, abs=1e18)
	assert pytest.approx(dai.balanceOf(depositor), 500e18, abs=1e18)

	# Withdraw some DAI from another_depositor
	metaVault.withdraw(500e18, another_depositor, {'from': another_depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 500e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 500e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 0, abs=1e18)
	assert pytest.approx(dai.balanceOf(another_depositor), 500, abs=1e18)

	# Re-deposit some DAI from depositor and another_depositor
	dai.approve(metaVault.address, 500e18, {'from': depositor})
	assert dai.allowance(depositor, metaVault.address) == 500e18
	metaVault.deposit(500e18, depositor, {'from': depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 0, abs=1e18)
	assert pytest.approx(dai.balanceOf(depositor), 0, abs=1e18)
	dai.approve(metaVault.address, 500e18, {'from': another_depositor})
	assert dai.allowance(another_depositor, metaVault.address) == 500e18
	metaVault.deposit(500e18, another_depositor, {'from': another_depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1500e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 500e18, abs=1e18)
	assert pytest.approx(dai.balanceOf(another_depositor), 0, abs=1e18)
	print_situation('ether')

def dai_to_usdc():
	estimateOut = metaVault.estimate_out(VAULT_USDC, [[2, "0xad71Fc10Fca8Ce6a98843A64b95E0C63516CA7F3", 2, 1]])
	assert pytest.approx(estimateOut, 1000e18, abs=10e18)
	metaVault.swap(
		VAULT_USDC,
		estimateOut * 90 / 100,
		[[2, "0xad71Fc10Fca8Ce6a98843A64b95E0C63516CA7F3", 2, 1]],
		{'from': deployer}
	)
	assert pytest.approx(metaVault.power(), 1e18, abs=1e17)
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1000e6, abs=1e6)
	assert pytest.approx(metaVault.getShares(depositor), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 500e18, abs=1e18)
	print_situation('mwei')

def usdc_to_mim():
	estimateOut = metaVault.estimate_out(VAULT_MIM, [[2, "0x2dd7C9371965472E5A5fD28fbE165007c61439E1", 2, 0]])
	assert pytest.approx(estimateOut, 1000e18, abs=10e18)
	metaVault.swap(
		VAULT_MIM,
		estimateOut * 90 / 100,
		[[2, "0x2dd7C9371965472E5A5fD28fbE165007c61439E1", 2, 0]],
		{'from': deployer}
	)
	assert pytest.approx(metaVault.power(), 1e18, abs=1e17)
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 500e18, abs=1e18)
	print_situation('ether')

def mim_to_dai():
	estimateOut = metaVault.estimate_out(VAULT_DAI, [[2, "0xad71Fc10Fca8Ce6a98843A64b95E0C63516CA7F3", 3, 2]])
	assert pytest.approx(estimateOut, 1000e18, abs=10e18)
	metaVault.swap(
		VAULT_DAI,
		estimateOut * 90 / 100,
		[[2, "0xad71Fc10Fca8Ce6a98843A64b95E0C63516CA7F3", 3, 2]],
		{'from': deployer}
	)
	assert pytest.approx(metaVault.power(), 1e18, abs=1e17)
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 500e18, abs=1e18)
	print_situation('ether')

def main():
	init_metavault()
	dai_to_usdc()
	simulate_harvest(usdc, BIG_WHALE_USDC, VAULT_USDC)
	print_situation('mwei')
	usdc_to_mim()
	mim_to_dai()