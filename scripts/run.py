import pytest
from brownie import MetaVault, VaultSwapper, Contract, Wei, accounts, chain, convert

PATH_HBTC_TO_USDT = [[1, "0x4CA9b3063Ec5866A4B82E437059D2C43d1be596F", 1, 0], [2, '0x80466c64868E1ab14a1Ddf27A676C3fcBE638Fe5', 1, 0]]

curveHBTCToken = "0xb19059ebb43466c323583928285a49f558e572fd"
curveHBTCTokenWhale = "0x4c18e409dc8619bfb6a1cb56d114c3f592e0ae79"

curveUSDTToken = "0xdac17f958d2ee523a2206206994597c13d831ec7"


deployer = accounts[0]
depositor = accounts[1]
another_depositor = accounts[2]
bowswap = deployer.deploy(VaultSwapper)
bowswap.initialize(deployer, {"from": deployer})
metaVault = deployer.deploy(MetaVault, curveHBTCToken, bowswap)
eurs = Contract.from_explorer(curveHBTCToken)
# usdc = Contract.from_explorer(TOKEN_USDC)

def simulate_harvest(token, whale, vault):
	print('SIMULATING HARVEST WITH 100_000_000 USDC EARNED')
	token.transfer(vault, 100000000e18, {'from': whale})

def print_situation():
	vaultPPS = float('{0:.2f}'.format(metaVault.underlyingPricePerShare().to('ether')))
	depositorShare = float('{0:.2f}'.format(metaVault.getShares(depositor).to('ether')))
	anotherDepositorShare = float('{0:.2f}'.format(metaVault.getShares(another_depositor).to('ether')))
	print('--------------------------------')
	print('TotalShare: ' + convert.to_string(metaVault.metaVaultTotalShare().to('ether')))
	print('Underlying PPS: ' + convert.to_string(metaVault.underlyingPricePerShare().to('ether')))
	print('Depositor Share: ' + convert.to_string(metaVault.getShares(depositor).to('ether')) + ' (' + str(round(vaultPPS * depositorShare)) + '$)')
	print('Another Depositor Share: ' + convert.to_string(metaVault.getShares(another_depositor).to('ether')) + ' (' + str(round(vaultPPS * anotherDepositorShare)) + '$)')
	print('--------------------------------')

def init_metavault():
	assert metaVault.metaVaultTotalShare() == 0
	assert metaVault.getShares(depositor) == 0

	# Take some eurs from the whales to work with
	eurs.transfer(depositor, 1e18, {'from': curveHBTCTokenWhale})
	assert eurs.balanceOf(depositor) >= 1e18
	eurs.transfer(another_depositor, 0.5e18, {'from': curveHBTCTokenWhale})
	assert eurs.balanceOf(another_depositor) >= 0.5e18

	# Deposit some eurs from depositor
	eurs.approve(metaVault.address, 1e18, {'from': depositor})
	assert eurs.allowance(depositor, metaVault.address) == 1e18
	metaVault.deposit(1e18, depositor, {'from': depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 1e18, abs=1e18)

	print_situation()

	# Deposit some eurs from another_depositor
	eurs.approve(metaVault.address, 0.5e18, {'from': another_depositor})
	assert eurs.allowance(another_depositor, metaVault.address) == 0.5e18
	metaVault.deposit(0.5e18, another_depositor, {'from': another_depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 10.5e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 1e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 0.5e18, abs=1e18)

	# Withdraw some eurs from depositor
	metaVault.withdraw(0.5e18, depositor, {'from': depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 0.5e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 0.5e18, abs=1e18)
	assert pytest.approx(eurs.balanceOf(depositor), 0.5e18, abs=1e18)

	# Withdraw some eurs from another_depositor
	metaVault.withdraw(0.5e18, another_depositor, {'from': another_depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 0.5e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 0.5e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 0, abs=1e18)
	assert pytest.approx(eurs.balanceOf(another_depositor), 500, abs=1e18)

	# Re-deposit some eurs from depositor and another_depositor
	eurs.approve(metaVault.address, 0.5e18, {'from': depositor})
	assert eurs.allowance(depositor, metaVault.address) == 0.5e18
	metaVault.deposit(0.5e18, depositor, {'from': depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 1e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 0, abs=1e18)
	assert pytest.approx(eurs.balanceOf(depositor), 0, abs=1e18)
	eurs.approve(metaVault.address, 0.5e18, {'from': another_depositor})
	assert eurs.allowance(another_depositor, metaVault.address) == 0.5e18
	metaVault.deposit(0.5e18, another_depositor, {'from': another_depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 10.5e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 1e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 0.5e18, abs=1e18)
	assert pytest.approx(eurs.balanceOf(another_depositor), 0, abs=1e18)
	print_situation()

def migrate(to, path):
	estimateOut = metaVault.estimateMigration(to, path)
	assert pytest.approx(estimateOut, 1e18, abs=1e18)
	metaVault.swap(to, estimateOut * 0.1, path, {'from': deployer})
	assert pytest.approx(metaVault.power(), 1e18, abs=1e17)
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 1e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 0.5e18, abs=1e18)
	print_situation()

def main():
	init_metavault()
	migrate(to = curveUSDTToken, path = PATH_HBTC_TO_USDT)


# bowswap.estimate_out("0x625b7DF2fa8aBe21B0A976736CDa4775523aeD1E", "0x7Da96a3891Add058AdA2E826306D812C638D87a7", 1e18, PATH_HBTC_TO_USDT, 30)