Name     : cri-containerd
Version  : 0
Release  : 2
URL      : https://github.com/containerd/cri-containerd/archive/v1.0.0-beta.1.tar.gz
Source0  : https://github.com/containerd/cri-containerd/archive/v1.0.0-beta.1.tar.gz
Summary  : Containerd-based implementation of Kubernetes Container Runtime Interface
Group    : Development/Tools
License  : Apache-2.0
BuildRequires: btrfs-progs-dev
BuildRequires: glibc-staticdev
BuildRequires: go
BuildRequires: libseccomp-dev
Requires: cni
Requires: containerd
Requires: runc

%global goroot /usr/lib/golang
%global library_path github.com/cri-containerd

%description
cri-containerd is a containerd based implementation of Kubernetes container runtime interface (CRI).

With it, you could run Kubernetes using containerd as the container runtime. 

%package dev
Summary: dev components for the containerd package.
Group: Development

%description dev
dev components for the containerd package.

%prep
%setup -q -n cri-containerd-1.0.0-beta.1

%build
export GOPATH=/go AUTO_GOPATH=1
mkdir -p /go/src/github.com/kubernetes-incubator/
ln -s /builddir/build/BUILD/%{name}-1.0.0-beta.1 /go/src/github.com/kubernetes-incubator/cri-containerd
pushd /go/src/github.com/kubernetes-incubator/cri-containerd
make V=1 %{?_smp_mflags} BUILD_TAGS='seccomp'
popd

%install
rm -rf %{buildroot}
%make_install BINDIR=%{buildroot}/usr/bin

# Copy all *.go, *.s and *.proto files
install -d -p %{buildroot}%{goroot}/src/%{library_path}/
for ext in go s proto; do
	for file in $(find . -iname "*.$ext" | grep -v "^./Godeps") ; do
		install -d -p %{buildroot}%{goroot}/src/%{library_path}/$(dirname $file)
		cp -pav $file %{buildroot}%{goroot}/src/%{library_path}/$file
	done
done

%files
%defattr(-,root,root,-)
/usr/bin/cri-containerd

%files dev
%defattr(-,root,root,-)
%{goroot}/src/%{library_path}/*
