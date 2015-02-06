%define modname oggvorbis
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A23_%{modname}.ini

Summary:	PHP OGG wrapper for OGG/Vorbis files
Name:		php-%{modname}
Version:	0.2
Release:	36
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/oggvorbis
Source0:	%{modname}-%{version}.tar.bz2
Source1:	%{modname}.ini.bz2
Patch0:		oggvorbis-0.2-label_at_end_of_compound_statement.diff
BuildRequires:	oggvorbis-devel
BuildRequires:	libogg-devel
BuildRequires:	php-devel >= 3:5.2.0
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
fopen wrapper for OGG/Vorbis files. Decompress OGG data to PCM audio and
vice-versa.

%prep

%setup -q -n %{modname}-%{version}
%patch0 -p0

%build
%serverbuild

%{_usrsrc}/php-devel/buildext %{modname} "%{modname}.c" \
    "-logg -lvorbis -lvorbisenc -lvorbisfile" \
    "-DWITH_OGGVORBIS -DCOMPILE_DL_OGGVORBIS" \
    "-I%{_includedir}/vorbis -I%{_includedir}/ogg"

#phpize
#%%configure2_5x --with-libdir=%{_lib} \
#    --with-%{modname}=shared,%{_prefix}
#
#%%make
#mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

cat > README.%{modname} << EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
EOF

bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-35mdv2012.0
+ Revision: 795483
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-34
+ Revision: 761275
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-33
+ Revision: 696452
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-32
+ Revision: 695447
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-31
+ Revision: 646668
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-30mdv2011.0
+ Revision: 629842
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-29mdv2011.0
+ Revision: 628169
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-28mdv2011.0
+ Revision: 600515
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-27mdv2011.0
+ Revision: 588853
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-26mdv2010.1
+ Revision: 514584
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-25mdv2010.1
+ Revision: 485413
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-24mdv2010.1
+ Revision: 468201
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-23mdv2010.0
+ Revision: 451311
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1:0.2-22mdv2010.0
+ Revision: 397305
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-21mdv2010.0
+ Revision: 377010
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-20mdv2009.1
+ Revision: 346523
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-19mdv2009.1
+ Revision: 341782
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-18mdv2009.1
+ Revision: 321882
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-17mdv2009.1
+ Revision: 310291
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-16mdv2009.0
+ Revision: 238416
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-15mdv2009.0
+ Revision: 200254
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-14mdv2008.1
+ Revision: 162142
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-13mdv2008.1
+ Revision: 107699
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-12mdv2008.0
+ Revision: 77564
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-11mdv2008.0
+ Revision: 39512
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-10mdv2008.0
+ Revision: 33866
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-9mdv2008.0
+ Revision: 21345
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-8mdv2007.0
+ Revision: 117603
- rebuilt against new upstream version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-7mdv2007.0
+ Revision: 78094
- rebuilt for php-5.2.0
- Import php-oggvorbis

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-6
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-5mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2-4mdk
- rebuilt for php-5.1.3

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-3mdk
- rebuilt against php-5.1.2

* Wed Nov 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-2mdk
- rebuilt against php-5.1.1

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-1mdk
- rebuilt against php-5.1.0
- fix versioning

* Sun Oct 02 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_0.2-0.RC1.1mdk
- rebuilt against php-5.1.0RC1

* Wed Sep 07 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.5_0.2-1mdk
- rebuilt against php-5.0.5 (Major security fixes)

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_0.2-1mdk
- rename the package

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_0.2-1mdk
- 5.0.4

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_0.2-2mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_0.2-1mdk
- initial Mandrakelinux package

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.2-3mdk
- rebuilt against a non hardened-php aware php lib

* Sat Jan 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.2-2mdk
- rebuild due to hardened-php-0.2.6
- cleanups

* Thu Dec 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.2-1mdk
- rebuild for php 4.3.10

* Sat Oct 02 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.9_0.2-1mdk
- rebuild for php 4.3.9

* Thu Jul 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_0.2-1mdk
- rebuilt for php-4.3.8

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_0.2-2mdk
- remove redundant provides

* Mon Jun 21 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_0.2-1mdk
- rebuilt for php-4.3.7
- added P0

* Mon May 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_0.2-2mdk
- use the %%configure2_5x macro
- move scandir to /etc/php.d

* Thu May 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_0.2-1mdk
- built for php 4.3.6

