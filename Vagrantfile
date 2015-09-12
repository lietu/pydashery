# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    # We're using Debian wheezy as that's what Raspbian is based on
    # https://www.raspbian.org/RaspbianFAQ
    config.vm.box = "debian/wheezy64"
    config.vm.boot_timeout = 30

    # SSH agent forwarding makes life easier
    config.ssh.forward_agent = true

    config.vm.network :private_network, ip: "172.25.49.27"

    # Configure Salt stack
    config.vm.provision :salt do |config|
        config.install_type = 'stable'
    end

    # Define the vm
    config.vm.define :pydashery do |pydashery|
        pydashery.vm.hostname = "pydashery"

        pydashery.vm.synced_folder "salt/roots/", "/srv/"
        pydashery.vm.synced_folder ".", "/src/"

        pydashery.vm.provider "virtualbox" do |v|
            v.name = "pydashery"
            # Uncomment if you want to see the virtualbox Gui for this VM
            # v.gui = true
            v.customize ["modifyvm", :id, "--memory", "256"]
            v.customize ["modifyvm", :id, "--cpus", "4"]
            v.customize ["modifyvm", :id, "--ioapic", "on"]
        end

        pydashery.vm.provision :salt do |config|
            config.minion_config = "salt/minion.conf"
            config.run_highstate = true
            config.verbose = false
            config.bootstrap_options = "-F -c /tmp -D"
            config.install_type = "git"
            config.install_args = "develop"
            config.temp_config_dir = "/tmp"
            config.colorize = true
            config.log_level = "info"

            config.pillar({
                vagrant: "vagrant"
            })
        end
    end
end
