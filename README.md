# Derivative APT Repository Command Line Interface (CLI) #

This tool can always be used to enable either Derivative's stable, testers or
developers repository or to disable Derivative's repository.

Derivative's APT Repository is not enabled by default. Some users prefer this
for trust/security reasons.

On first boot of Derivative, the Derivative Repository Tool gets automatically
started by setup-dist. The user is free to either leave Derivative's
repository disabled or to configure it as desired.

Technically speaking, this tool creates or deletes file
`/etc/sources.list.d/derivative.list`.

Using APT `signed-by`.
## How to install `repository-dist` using apt-get ##

1\. Download Whonix's Signing Key.

```
wget https://www.whonix.org/patrick.asc
```

Users can [check Whonix Signing Key](https://www.whonix.org/wiki/Whonix_Signing_Key) for better security.

2\. Add Whonix's signing key.

```
sudo cp ~/derivative.asc /usr/share/keyrings/derivative.asc
```

3\. Add Whonix's APT repository.

```
echo "deb [signed-by=/usr/share/keyrings/derivative.asc] https://deb.whonix.org bullseye main contrib non-free" | sudo tee /etc/apt/sources.list.d/derivative.list
```

4\. Update your package lists.

```
sudo apt-get update
```

5\. Install `repository-dist`.

```
sudo apt-get install repository-dist
```

## How to Build deb Package from Source Code ##

Can be build using standard Debian package build tools such as:

```
dpkg-buildpackage -b
```

See instructions. (Replace `generic-package` with the actual name of this package `repository-dist`.)

* **A)** [easy](https://www.whonix.org/wiki/Dev/Build_Documentation/generic-package/easy), _OR_
* **B)** [including verifying software signatures](https://www.whonix.org/wiki/Dev/Build_Documentation/generic-package)

## Contact ##

* [Free Forum Support](https://forums.whonix.org)
* [Professional Support](https://www.whonix.org/wiki/Professional_Support)

## Donate ##

`repository-dist` requires [donations](https://www.whonix.org/wiki/Donate) to stay alive!
