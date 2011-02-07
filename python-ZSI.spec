

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global with_python26 1
%if %{?with_python26}
%global __python26 %{_bindir}/python2.6
%global py26dir  %{_builddir}/python26-%{name}-%{version}-%{release}
%global python26_sitelib     /usr/lib/python2.6/site-packages
# Disable byte compiling. Do ourselves later.
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g') 
%endif

Name:           python-ZSI
Version:        2.0
Release:        7%{?dist}
Summary:        Zolera SOAP Infrastructure
Group:          Development/Languages
# to obtain some license information have a look at ZSI/__init__.py file
License:        MIT and LBNL BSD and ZPLv2.0
URL:            http://pywebsvcs.sourceforge.net/
Source0:        http://belnet.dl.sourceforge.net/sourceforge/pywebsvcs/ZSI-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel python-setuptools
BuildRequires:  python26-devel python26-distribute
Requires:       PyXML

%description
The Zolara SOAP Infrastructure provides libraries for developing web services
using the python programming language. The libraries implement the various
protocols used when writing web services including SOAP, WSDL, and other
related protocols.

%if %{?with_python26}
%package -n python26-ZSI
Summary:        Zolera SOAP Infrastructure for Python 2.6
Group:          Development/Languages
Requires:       python26-PyXML
Requires:       python(abi) = 2.6

%description -n python26-ZSI
The Zolara SOAP Infrastructure provides libraries for developing web services
using the python programming language. The libraries implement the various
protocols used when writing web services including SOAP, WSDL, and other
related protocols.

This package is a python2.6 module.
%endif

%prep
%setup -q -n ZSI-%{version}

# remove cvs internal files and
# get rid of executable perm due to rpmlint's
# warnings like: 
# W: python-zsi spurious-executable-perm
#

find doc/examples -name .cvs\* -exec rm -f {} \;
find doc/examples samples -perm 755 -type f -exec chmod a-x {} \;

%if 0%{?with_python26}
%{__rm} -rf %{py26dir}
cp -a . %{py26dir}
%endif

%build
%{__python} setup.py build

%if 0%{?with_python26}
pushd %{py26dir}
%{__python26} setup.py build
popd
%endif


%install
rm -rf $RPM_BUILD_ROOT

%if 0%{?with_python26}
pushd %{py26dir}
%{__python26} setup.py install -O1 --skip-build --root %{buildroot}
find $RPM_BUILD_ROOT%{python26_sitelib}/ZSI \
    -type f -perm 644 -name \*.py \
    -exec grep -q \#\!\.\*python {} \; \
    -and -exec chmod a+x {} \;
popd
%endif

rm -f  %{buildroot}%{_bindir}/wsdl2dispatch
rm -f  %{buildroot}%{_bindir}/wsdl2py

%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# some files have shebang and aren't executable
# the simple command below looks for them and if
# they're found, it'll do chmod a+x

find $RPM_BUILD_ROOT%{python_sitelib}/ZSI \
    -type f -perm 644 -name \*.py \
    -exec grep -q \#\!\.\*python {} \; \
    -and -exec chmod a+x {} \;
 
%if 0%{?with_python26}
%{__python} -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT"'", 10, "%{python_sitelib}", 1)' > /dev/null
%{__python} -O -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT"'", 10, "%{python_sitelib}", 1)' > /dev/null
%{__python26} -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT%{python26_sitelib}"'", 10, "%{python26_sitelib}", 1)' > /dev/null
%{__python26} -O -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT%{python26_sitelib}"'", 10, "%{python26_sitelib}", 1)' > /dev/null
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
# we need png's for html's to be more readable
%doc CHANGES README samples doc/examples doc/*.html doc/*.png doc/*.css
%{_bindir}/wsdl2dispatch
%{_bindir}/wsdl2py
%{python_sitelib}/ZSI
%{python_sitelib}/ZSI-*.egg-info

%if 0%{?with_python26}
%files -n python26-ZSI
%defattr(-,root,root,-)
# we need png's for html's to be more readable
%doc CHANGES README samples doc/examples doc/*.html doc/*.png doc/*.css
%{python26_sitelib}/ZSI
%{python26_sitelib}/ZSI-*.egg-info
%endif



%changelog
* Mon Feb 7 2011 Steve Traylen <steve.traylen@cern.ch> - 2.0-7
- Add python26 package.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0-4
- Rebuild for Python 2.6

* Fri Jan 04 2008 Michał Bentkowski <mr.ecik at gmail.com> - 2.0-3
- Just bumping...

* Sat Dec 29 2007 Michał Bentkowski <mr.ecik at gmail.com> - 2.0-2
- Fix License field (BSD to LBNL BSD)

* Thu Nov 01 2007 Michał Bentkowski <mr.ecik at gmail.com> - 2.0-1
- First release

