import pytest
from brownie import MetaVault, VaultSwapper, Contract, Wei, accounts, chain, convert

PATH_EURS_TO_EURT = [[1, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 1, 0], [0, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 1, 0]]
PATH_EURS_TO_IBEUR = [[1, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 1, 0], [0, "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859", 1, 0]]
PATH_EURS_TO_EURN = [[1, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 0, 0], [2, "0x3CFAa1596777CAD9f5004F9a0c443d912E262243", 2, 1], [0, "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a", 1, 0]]
PATH_EURS_TO_3EUR = [[1, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 0, 0], [0, "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571", 2, 0]]

PATH_EURT_TO_EURS = [[1, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 1, 0], [0, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 1, 0]]
PATH_EURT_TO_IBEUR = [[1, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 1, 0], [0, "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859", 1, 0]]
PATH_EURT_TO_EURN = [[1, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 0, 0], [0, "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a", 1, 0]]
PATH_EURT_TO_3EUR = [[1, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 0, 0], [0, "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571", 1, 0]]

PATH_IBEUR_TO_EURS = [[1, "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859", 1, 0], [0, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 1, 0]]
PATH_IBEUR_TO_EURT = [[1, "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859", 1, 0], [0, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 1, 0]]
PATH_IBEUR_TO_EURN = [[1, "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859", 1, 0], [2, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 1, 0], [0, "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a", 1, 0]]
PATH_IBEUR_TO_3EUR = [[1, "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859", 0, 0], [2, "0xB37D6c07482Bc11cd28a1f11f1a6ad7b66Dec933", 0, 1], [0, "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571", 0, 0]]

PATH_EURN_TO_EURS = [[1, "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a", 1, 0], [2, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 0, 1], [0, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 1, 0]]
PATH_EURN_TO_EURT = [[1, "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a", 1, 0], [0, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 0, 0]]
PATH_EURN_TO_IBEUR = [[1, "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a", 1, 0], [2, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 0, 1], [0, "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859", 1, 0]]
PATH_EURN_TO_3EUR = [[1, "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a", 1, 0], [0, "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571", 1, 0]]

PATH_3EUR_TO_EURS = [[1, "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571", 2, 0], [0, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 0, 0]]
PATH_3EUR_TO_EURT = [[1, "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571", 1, 0], [0, "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", 0, 0]]
PATH_3EUR_TO_IBEUR = [[1, "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571", 0, 0], [2, "0x45a8CC73EC100306af64AB2CcB7B12E70EC549A8", 0, 1], [0, "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859", 1, 0]]
PATH_3EUR_TO_EURN = [[1, "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571", 1, 0], [0, "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a", 1, 0]]


# 0x80466c64868E1ab14a1Ddf27A676C3fcBE638Fe5


curveEURSToken = "0x194eBd173F6cDacE046C53eACcE9B953F28411d1"
curveEURSTokenWhale = "0x90bb609649e0451e5ad952683d64bd2d1f245840"

curveEURTToken = "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890"
curveibEURToken = "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859"
curveEURNToken = "0x3Fb78e61784C9c637D560eDE23Ad57CA1294c14a"
curve3EURToken = "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571"

deployer = accounts[0]
depositor = accounts[1]
another_depositor = accounts[2]
bowswap = deployer.deploy(VaultSwapper)
bowswap.initialize(deployer, {"from": deployer})
metaVault = deployer.deploy(MetaVault, curveEURSToken, bowswap)
eurs = Contract.from_explorer(curveEURSToken)
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
	eurs.transfer(depositor, 1000e18, {'from': curveEURSTokenWhale})
	assert eurs.balanceOf(depositor) >= 1000e18
	eurs.transfer(another_depositor, 500e18, {'from': curveEURSTokenWhale})
	assert eurs.balanceOf(another_depositor) >= 500e18

	# Deposit some eurs from depositor
	eurs.approve(metaVault.address, 1000e18, {'from': depositor})
	assert eurs.allowance(depositor, metaVault.address) == 1000e18
	metaVault.deposit(1000e18, depositor, {'from': depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 1000e18, abs=1e18)

	print_situation()

	# Deposit some eurs from another_depositor
	eurs.approve(metaVault.address, 500e18, {'from': another_depositor})
	assert eurs.allowance(another_depositor, metaVault.address) == 500e18
	metaVault.deposit(500e18, another_depositor, {'from': another_depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1500e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 500e18, abs=1e18)

	# Withdraw some eurs from depositor
	metaVault.withdraw(500e18, depositor, {'from': depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 500e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 500e18, abs=1e18)
	assert pytest.approx(eurs.balanceOf(depositor), 500e18, abs=1e18)

	# Withdraw some eurs from another_depositor
	metaVault.withdraw(500e18, another_depositor, {'from': another_depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 500e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 500e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 0, abs=1e18)
	assert pytest.approx(eurs.balanceOf(another_depositor), 500, abs=1e18)

	# Re-deposit some eurs from depositor and another_depositor
	eurs.approve(metaVault.address, 500e18, {'from': depositor})
	assert eurs.allowance(depositor, metaVault.address) == 500e18
	metaVault.deposit(500e18, depositor, {'from': depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 0, abs=1e18)
	assert pytest.approx(eurs.balanceOf(depositor), 0, abs=1e18)
	eurs.approve(metaVault.address, 500e18, {'from': another_depositor})
	assert eurs.allowance(another_depositor, metaVault.address) == 500e18
	metaVault.deposit(500e18, another_depositor, {'from': another_depositor})
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1500e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(depositor), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 500e18, abs=1e18)
	assert pytest.approx(eurs.balanceOf(another_depositor), 0, abs=1e18)
	print_situation()

def migrate(to, path):
	estimateOut = metaVault.estimateMigration(to, path)
	assert pytest.approx(estimateOut, 1000e18, abs=10e18)
	metaVault.swap(to, estimateOut * 0.1, path, {'from': deployer})
	assert pytest.approx(metaVault.power(), 1e18, abs=1e17)
	assert pytest.approx(metaVault.metaVaultTotalShare(), 1000e6, abs=1e6)
	assert pytest.approx(metaVault.getShares(depositor), 1000e18, abs=1e18)
	assert pytest.approx(metaVault.getShares(another_depositor), 500e18, abs=1e18)
	print_situation()

def main():
	init_metavault()
	migrate(to = curveEURTToken, path = PATH_EURS_TO_EURT)
	migrate(to = curveibEURToken, path = PATH_EURT_TO_IBEUR)
	migrate(to = curveEURNToken, path = PATH_IBEUR_TO_EURN)
	migrate(to = curve3EURToken, path = PATH_EURN_TO_3EUR)
	migrate(to = curveEURSToken, path = PATH_3EUR_TO_EURS)
	migrate(to = curveEURNToken, path = PATH_EURS_TO_EURN)
	migrate(to = curveEURTToken, path = PATH_EURN_TO_EURT)

