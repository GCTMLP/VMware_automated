from pyVim.connect import *

def power_on(host, user, pwd, name_vm):
	c = SmartConnectNoSSL(host=host, user=user, pwd=pwd)
	content = c.content
	container_vms = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
	for vm in container_vms.view:
		if vm.name == name_vm:
			my_vm = vm
			if vm.summary.runtime.powerState == 'poweredOff':
				vm.PowerOn()
			else:
				print(vm.name+" is already powered")


def power_off(host, user, pwd, name_vm):
	c = SmartConnectNoSSL(host=host, user=user, pwd=pwd)
	content = c.content
	container_vms = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
	for vm in container_vms.view:
		if vm.name == name_vm:
			my_vm = vm
			print(vm.summary.runtime.powerState)
			if vm.summary.runtime.powerState == 'poweredOn':
				vm.PowerOff()
			else:
				print(vm.name+" is already powered Off")

