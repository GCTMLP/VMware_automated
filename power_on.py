from pyVim.connect import SmartConnectNoSSL
from pyVmomi import vim

def power_on(host, user, pwd, name_vm):
	"""
	function to power on VM
	:param host: host ip
	:param user: esxi host user
	:param pwd: esxi host password
	:param name_vm: vm`s name

	:return: None
	"""
	c = SmartConnectNoSSL(host=host, user=user, pwd=pwd)
	content = c.content
	container_vms = content.viewManager.\
		CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
	for vm in container_vms.view:
		if vm.name == name_vm:
			if vm.summary.runtime.powerState == 'poweredOff':
				vm.PowerOn()
			else:
				print(vm.name+" is already powered")


def power_off(host, user, pwd, name_vm):
	"""
		function to power off VM
		:param host: host ip
		:param user: esxi host user
		:param pwd: esxi host password
		:param name_vm: vm`s name

		:return: None
		"""
	c = SmartConnectNoSSL(host=host, user=user, pwd=pwd)
	content = c.content
	container_vms = content.viewManager.\
		CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
	for vm in container_vms.view:
		if vm.name == name_vm:
			if vm.summary.runtime.powerState == 'poweredOn':
				vm.PowerOff()
			else:
				print(vm.name+" is already powered Off")
