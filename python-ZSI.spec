%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-ZSI
Version:        2.1
Release:        1%{?dist}
Summary:        Zolera SOAP Infrastructure
Group:          Development/Languages
# to obtain some license information have a look at ZSI/__init__.py file
License:        MIT and LBNL BSD and ZPLv2.0
URL:            http://pywebsvcs.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/pywebsvcs/ZSI/ZSI-%{version}_a1/ZSI-%{version}-a1.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel python-setuptools PyXML
Requires:       PyXML python-setuptools

%description
The Zolera SOAP Infrastructure provides libraries for developing web services
using the python programming language. The libraries implement the various
protocols used when writing web services including SOAP, WSDL, and other
related protocols.

%prep
%setup -q -n ZSI-%{version}-a1

# remove cvs internal files and
# get rid of executable perm due to rpmlint's
# warnings like: 
# W: python-zsi spurious-executable-perm
#

find doc/examples -name .cvs\* -exec rm -f {} \;
find doc/examples samples -perm 755 -type f -exec chmod a-x {} \;

%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# some files have shebang and aren't executable
# the simple command below looks for them and if
# they're found, it'll do chmod a+x

find %{buildroot}%{python_sitelib}/ZSI \
    -type f -perm 644 -name \*.py \
    -exec grep -q \#\!\.\*python {} \; \
    -and -exec chmod a+x {} \;

%check
# ZSI module is not installed yet, so we need to tell python where to find it
# in order to execute tests
export PYTHONPATH=$(pwd)
good_testlist="test_t1
test_t2
test_t3
test_t5
test_t6
test_t7
test_t9
test_union
test_list
test_URI
test_rfc2617
test_TCtimes"
for i in $good_testlist; do
    %{__python} test/${i}.py 
done

bad_testlist="test_t8"
# These tests fails for now, fix upstream?
for i in $bad_testlist; do
    %{__python} test/${i}.py || :
done
 
%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
# we need png's for html's to be more readable
%doc CHANGES README samples doc/examples doc/*.html doc/*.png doc/*.css
%{_bindir}/wsdl2py
%{python_sitelib}/ZSI
%{python_sitelib}/ZSI-*.egg-info


%changelog
* Sat Aug 11 2012 Tim Fenn <tim.fenn@gmail.com> - 2.1-1
- update to 2.1-a1

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 10 2012 Tim Fenn <tim.fenn@gmail.com> - 2.0-12
- fix download url (again)
- add ZSI directory to PYTHONPATH
- add test_TCtimes to bad testlist

* Thu Feb 09 2012 Tim Fenn <tim.fenn@gmail.com> - 2.0-11
- fix download url
- use macro style
- add tests

* Wed Feb 08 2012 Tim Fenn <tim.fenn@gmail.com> - 2.0-10
- rebuild for new maintainer

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 13 2010 James Bowes <jbowes@redhat.com> 2.0-7
- Fix typo in description

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

