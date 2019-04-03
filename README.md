# Whonix APT Repository Tool #

This tool can always be used to enable either Whonix's stable, testers or
developers repository or to disable Whonix's repository.

Whonix's APT Repository is not enabled by default. Some users prefer this for
trust/security reasons.

On first boot of Whonix, the Whonix Repository Tool gets automatically started
by whonixsetup. The user is free to either leave Whonix's repository disabled
or to configure it as desired.

Technically speaking, this tool creates or deletes
/etc/sources.list.d/whonix.list and adds or deletes Whonix's signing key from
apt-key.
## How to install `whonix-repository` using apt-get ##

1\. Add [Whonix's Signing Key](https://www.whonix.org/wiki/Whonix_Signing_Key).

```
sudo apt-key --keyring /etc/apt/trusted.gpg.d/whonix.gpg adv --keyserver hkp://ipv4.pool.sks-keyservers.net:80 --recv-keys 916B8D99C38EAF5E8ADC7A2A8D66066A2EEACCDA
```

3\. Add Whonix's APT repository.

```
echo "deb http://deb.whonix.org buster main" | sudo tee /etc/apt/sources.list.d/whonix.list
```

4\. Update your package lists.

```
sudo apt-get update
```

5\. Install `whonix-repository`.

```
sudo apt-get install whonix-repository
```

## How to Build deb Package ##

Replace `apparmor-profile-torbrowser` with the actual name of this package with `whonix-repository` and see [instructions](https://www.whonix.org/wiki/Dev/Build_Documentation/apparmor-profile-torbrowser).

## Contact ##

* [Free Forum Support](https://forums.whonix.org)
* [Professional Support](https://www.whonix.org/wiki/Professional_Support)

## Payments ##

`whonix-repository` requires [payments](https://www.whonix.org/wiki/Payments) to stay alive!
