# puppetscl3 builds

These build exist to bring Puppet to new versions of Ruby, through the power of
software collections.  You might want this due to improved performance of newer
MRI versions, e.g. on your puppet master.

The usual packages are built against the standard Ruby version, i.e. 1.8.7 on
EL6, and the paths used in the binary RPMs will only be loaded by the 1.8
version of Ruby.  By rebuilding these into a new collection, it can depend on
a newer version of Ruby provided from another collection (such as ruby193 or
ruby200).

## Using these builds

See the [copr build page](http://copr-fe.cloud.fedoraproject.org/coprs/domcleal/puppetscl3/).

## Using this repo

After checking out, use `./setup_sources.sh` to configure git annex remotes to
access binary files.

## Licence

Spec files are generally based on Fedora spec files, which means that unless a
spec file contains an explicit license attribution within it, it is available
under the MIT license.
