import logging
import pytest
from monitor import parse_process_VMZ
from monitor import parse_top

LOG_FORMAT = "%(levelname)s %(asctime)s %(funcName)s- %(message)s"

@pytest.fixture
#Creates the default cermony files
def supply_logger():
    logging.basicConfig(filename = "monitoring_test.log",
    level = logging.INFO,
    format = LOG_FORMAT,
    filemode = 'w')

    logger = logging.getLogger()
    return logger

OUTPUT_PSAUX = """  PID USER       VSZ STAT COMMAND
    1 root      3244 S    init
    2 root         0 SW   [kthreadd]
    3 root         0 SW   [ksoftirqd/0]
    5 root         0 SW<  [kworker/0:0H]
    7 root         0 SW   [rcu_preempt]
    8 root         0 SW   [rcu_sched]
    9 root         0 SW   [rcu_bh]
   10 root         0 SW   [migration/0]
   11 root         0 SW   [watchdog/0]
   12 root         0 SW   [watchdog/1]
   13 root         0 SW   [migration/1]
   14 root         0 SW   [ksoftirqd/1]
   16 root         0 SW<  [kworker/1:0H]
   17 root         0 SW   [watchdog/2]
   18 root         0 SW   [migration/2]
   19 root         0 SW   [ksoftirqd/2]
   21 root         0 SW<  [kworker/2:0H]
   22 root         0 SW   [watchdog/3]
   23 root         0 SW   [migration/3]
   24 root         0 SW   [ksoftirqd/3]
   25 root         0 SW   [kworker/3:0]
   26 root         0 SW<  [kworker/3:0H]
   27 root         0 SW<  [khelper]
   28 root         0 SW   [kdevtmpfs]
  135 root         0 SW<  [writeback]
  137 root         0 SW<  [crypto]
  139 root         0 SW<  [bioset]
  141 root         0 SW<  [kblockd]
  155 root         0 SW   [skb_free_task]
  177 root         0 SWN  [kswapd0]
  178 root         0 SW   [fsnotify_mark]
  179 root         0 SW   [ecryptfs-kthrea]
  309 root         0 SW<  [linkwatch]
  310 root         0 SW<  [ipv6_addrconf]
  321 root         0 SW<  [deferwq]
  327 root         0 SW   [ubi_bgt0d]
  332 root         0 SW   [kworker/3:1]
  351 root         0 SW<  [kworker/2:1H]
  352 root         0 SW<  [kworker/0:1H]
  353 root         0 SW<  [kworker/1:1H]
  369 root      3244 S    /bin/sh /etc/init.d/rcS S boot
  370 root      3244 S    /sbin/getty 115200 ttyAMA0
  372 root      3372 S    logger -s -p 6 -t sysinit
  392 root         0 SW   [ubi_bgt1d]
  443 root         0 SW   [ubi_bgt2d]
  539 root         0 SW   [ubifs_bgt2_0]
  763 root         0 SW<  [cfg80211]
  902 root      7612 S    firewall-app
  933 root         0 SW   [fc_evt]
  934 root         0 SW   [fc_timer]
  935 root         0 SW   [bcmFlwStatsTask]
  945 root         0 SW   [bcm_archer_us]
  946 root         0 SW   [bcm_archer_wlan]
  958 root         0 SW   [bcmsw_rx]
  959 root         0 SW   [bcmsw_recycle]
  960 root         0 SW   [enet-kthrd]
 1014 root         0 SW   [dhd_watchdog_th]
 1045 root         0 SW   [wl1-kthrd]
 1052 root         0 SW   [wl2-kthrd]
 1188 root      3768 S    syslog-ng -p /var/run/syslog-ng.pid
 1191 ism       7888 S    /usr/sbin/ismd
 1207 root      3244 S    /bin/sh /usr/bin/hg6d_start
 1209 root     50596 S    hg6d
 1632 root     10196 S    wshd +105601+NQ04800383
 1636 root     10188 S    wstd +105601+NQ04800383
 2320 root      3068 S    /usr/sbin/rdisc6 -i BR_LAN -l BR_LAN -r 3 -w 4
 2771 root         0 SW   [kworker/u8:2]
 3744 root      3260 S    /usr/sbin/radvd -n -C /etc/radvd.conf
 3750 root      3132 S    /usr/sbin/radvd -n -C /etc/radvd.conf
 3872 root      5636 S    hostapd /tmp/wl1_hapd.conf
 3875 root      5636 S    hostapd /tmp/wl2.1_hapd.conf
 6344 root         0 SW   [kworker/2:0]
 7337 root         0 SW   [kworker/u8:1]
 9046 dhcps4    5204 S    /usr/sbin/dhclient -d -cf /tmp/etc/dhclient_extender
 9047 root      5636 S    hostapd /tmp/wl0.2_hapd.conf
 9089 root      2004 S    mcpd
 9102 root      3588 S    dropbear -F -j -k -U root -p [192.168.1.100]:22 -P /
 9105 root      3244 S    telnetd -U root -b 192.168.1.100 -p 23 -F
 9131 nobody    3420 S    dnsmasq -k -b -c100 -r/tmp/relayresolv.conf --min-po
 9132 root      6320 S    /usr/sbin/lighttpd -f /etc/lighttpd/lighttpd.conf -D
11327 root         0 SW   [kworker/1:3]
13249 root         0 SW   [kworker/0:3]
14372 root         0 SW   [kworker/0:0]
16543 root      3716 S    dropbear -F -j -k -U root -p [192.168.1.100]:22 -P /
16556 root      3372 S    -ash
16699 root      3372 R    ps -aux
29992 root         0 SW   [kworker/1:1]
30049 root         0 SW   [kworker/2:1]
31408 root      2736 S    acsd2 -F
31409 root      2604 S    eapd -F
32136 root      4944 S    dhcrelay 192.168.1.1 -i BR_LAN --option6 192.168.1.9
"""

OUTPUT_PSAUX_M = """  PID USER       VSZ STAT COMMAND
    1 root      3244 S    init
    2 root         0 SW   [kthreadd]
    3 root         0 SW   [ksoftirqd/0]
    5 root         0 SW<  [kworker/0:0H]
    7 root         0 SW   [rcu_preempt]
    8 root         0 SW   [rcu_sched]
    9 root         0 SW   [rcu_bh]
   10 root         0 SW   [migration/0]
   11 root         0 SW   [watchdog/0]
   12 root         0 SW   [watchdog/1]
   13 root         0 SW   [migration/1]
   14 root         0 SW   [ksoftirqd/1]
   16 root         0 SW<  [kworker/1:0H]
   17 root         0 SW   [watchdog/2]
   18 root         0 SW   [migration/2]
   19 root         0 SW   [ksoftirqd/2]
   21 root         0 SW<  [kworker/2:0H]
   22 root         0 SW   [watchdog/3]
   23 root         0 SW   [migration/3]
   24 root         0 SW   [ksoftirqd/3]
   25 root         0 SW   [kworker/3:0]
   26 root         0 SW<  [kworker/3:0H]
   27 root         0 SW<  [khelper]
   28 root         0 SW   [kdevtmpfs]
  135 root         0 SW<  [writeback]
  137 root         0 SW<  [crypto]
  139 root         0 SW<  [bioset]
  141 root         0 SW<  [kblockd]
  155 root         0 SW   [skb_free_task]
  177 root         0 SWN  [kswapd0]
  178 root         0 SW   [fsnotify_mark]
  179 root         0 SW   [ecryptfs-kthrea]
  309 root         0 SW<  [linkwatch]
  310 root         0 SW<  [ipv6_addrconf]
  321 root         0 SW<  [deferwq]
  327 root         0 SW   [ubi_bgt0d]
  332 root         0 SW   [kworker/3:1]
  351 root         0 SW<  [kworker/2:1H]
  352 root         0 SW<  [kworker/0:1H]
  353 root         0 SW<  [kworker/1:1H]
  369 root      3244 S    /bin/sh /etc/init.d/rcS S boot
  370 root      3244 S    /sbin/getty 115200 ttyAMA0
  372 root      3372 S    logger -s -p 6 -t sysinit
  392 root         0 SW   [ubi_bgt1d]
  443 root         0 SW   [ubi_bgt2d]
  539 root         0 SW   [ubifs_bgt2_0]
  763 root         0 SW<  [cfg80211]
  902 root      7612 S    firewall-app
  933 root         0 SW   [fc_evt]
  934 root         0 SW   [fc_timer]
  935 root         0 SW   [bcmFlwStatsTask]
  945 root         0 SW   [bcm_archer_us]
  946 root         0 SW   [bcm_archer_wlan]
  958 root         0 SW   [bcmsw_rx]
  959 root         0 SW   [bcmsw_recycle]
  960 root         0 SW   [enet-kthrd]
 1014 root         0 SW   [dhd_watchdog_th]
 1045 root         0 SW   [wl1-kthrd]
 1052 root         0 SW   [wl2-kthrd]
 1188 root      3768 S    syslog-ng -p /var/run/syslog-ng.pid
 1191 ism       7888 S    /usr/sbin/ismd
 1207 root      3244 S    /bin/sh /usr/bin/hg6d_start
 1209 root     120m S    hg6d
 1632 root     10196 S    wshd +105601+NQ04800383
 1636 root     10188 S    wstd +105601+NQ04800383
 2320 root      3068 S    /usr/sbin/rdisc6 -i BR_LAN -l BR_LAN -r 3 -w 4
 2771 root         0 SW   [kworker/u8:2]
 3744 root      3260 S    /usr/sbin/radvd -n -C /etc/radvd.conf
 3750 root      3132 S    /usr/sbin/radvd -n -C /etc/radvd.conf
 3872 root      5636 S    hostapd /tmp/wl1_hapd.conf
 3875 root      5636 S    hostapd /tmp/wl2.1_hapd.conf
 6344 root         0 SW   [kworker/2:0]
 7337 root         0 SW   [kworker/u8:1]
 9046 dhcps4    5204 S    /usr/sbin/dhclient -d -cf /tmp/etc/dhclient_extender
 9047 root      5636 S    hostapd /tmp/wl0.2_hapd.conf
 9089 root      2004 S    mcpd
 9102 root      3588 S    dropbear -F -j -k -U root -p [192.168.1.100]:22 -P /
 9105 root      3244 S    telnetd -U root -b 192.168.1.100 -p 23 -F
 9131 nobody    3420 S    dnsmasq -k -b -c100 -r/tmp/relayresolv.conf --min-po
 9132 root      6320 S    /usr/sbin/lighttpd -f /etc/lighttpd/lighttpd.conf -D
11327 root         0 SW   [kworker/1:3]
13249 root         0 SW   [kworker/0:3]
14372 root         0 SW   [kworker/0:0]
16543 root      3716 S    dropbear -F -j -k -U root -p [192.168.1.100]:22 -P /
16556 root      3372 S    -ash
16699 root      3372 R    ps -aux
29992 root         0 SW   [kworker/1:1]
30049 root         0 SW   [kworker/2:1]
31408 root      2736 S    acsd2 -F
31409 root      2604 S    eapd -F
32136 root      4944 S    dhcrelay 192.168.1.1 -i BR_LAN --option6 192.168.1.9
"""

OUTPUT_HG6D_2 = """17098 root      3244 R    grep -w hg6d
1202 root     43168 S    hg6d
"""
OUTPUT_HG6D_6 = """17098 root      3244 R    grep -w hg6d
1202 root     43168 S    hg6d
"""

OUTPUT_HG6D_10 = """17098 root      3244 R    grep -w hg6d
1202 root     43168 R    hg6d
"""

OUTPUT_HG6D_7 = """17098 root      3244 R    grep -w hg6d
1202 root     143m S    hg6d
"""

OUTPUT_HG6D_8 = """17098 root      3244 R    grep -w hg6d
1202 root     143m R    hg6d
"""

OUTPUT_HG6D_1 = """1202 root     43168 S    hg6d
17098 root      3244 R    grep -w hg6d
"""
OUTPUT_HG6D_5 = """1202 root     43168 S    hg6d
17098 root      3244 S    grep -w hg6d
"""

OUTPUT_HG6D_9 = """1202 root     43168 R    hg6d
17098 root      3244 S    grep -w hg6d
"""

OUTPUT_HG6D_3 = """1202 root     143m S    hg6d
17098 root      3244 R    grep -w hg6d
"""
OUTPUT_HG6D_4 = """1202 root     143m R    hg6d
17098 root      3244 R    grep -w hg6d
"""

OUTPUT_HG6D_11 = """17098 root      3244 R    grep -w hg6d
"""

OUTPUT_HG6D_12 = """17098 root      3244 S    grep -w hg6d
"""

OUTPUT_HG6D_13 = """"""

def test_parse_vmz(supply_logger):
    """_summary_

    Args:
        supply_logger (_type_): _description_
    """
    row = {}
    parse_process_VMZ(OUTPUT_PSAUX, row, supply_logger)
    assert row["VMZ_HG6D"] == 50596
    assert row["VMZ_WSHD"] == 10196
    assert row["VMZ_WSTD"] == 10188
    assert row["VMZ_DHCLIENT"] == 5204
    assert row["VMZ_DHRELAY"] == 4944
    assert row["VMZ_ISMD"] == 7888
    assert row["VMZ_DNSMASQ"] == 3420

def test_parse_vmz2_m(supply_logger):
    """_summary_

    Args:
        supply_logger (_type_): _description_
    """
    row = {}
    parse_process_VMZ(OUTPUT_PSAUX_M, row, supply_logger)
    assert row["VMZ_HG6D"] == 120000000
    assert row["VMZ_WSHD"] == 10196
    assert row["VMZ_WSTD"] == 10188
    assert row["VMZ_DHCLIENT"] == 5204
    assert row["VMZ_DHRELAY"] == 4944
    assert row["VMZ_ISMD"] == 7888
    assert row["VMZ_DNSMASQ"] == 3420

OUTPUT_TOP_CMD = """Mem: 352032K used, 147752K free, 0K shrd, 22932K buff, 84676K cached
CPU:   0% usr   3% sys   0% nic  96% idle   0% io   0% irq   0% sirq
Load average: 0.80 0.56 0.65 2/110 6360
  PID  PPID USER     STAT   VSZ %VSZ %CPU COMMAND
  959   957 root     S    36512   7%   0% hg6d
 2020   959 root     S    30008   6%   0% /opt/prplmesh/bin/beerocks_agent
 2114     1 root     S    25272   5%   0% /opt/prplmesh/bin/beerocks_fronthaul -i wl0
 2116     1 root     S    25268   5%   0% /opt/prplmesh/bin/beerocks_fronthaul -i wl1
 1548   959 root     S    23624   5%   0% swand -n gtw
 1723   959 root     S    22532   5%   0% /opt/prplmesh/bin/beerocks_controller
 1416  1415 root     S    22524   5%   0% /usr/sbin/syslog-ng -p /var/run/syslog-ng.pid
 1021   959 root     S    20832   4%   0% /usr/sbin/halwifi
 1717   959 root     S    16136   3%   0% /opt/prplmesh/bin/ieee1905_transport controller_uds_broker
 2017   959 root     S    16136   3%   0% /opt/prplmesh/bin/ieee1905_transport agent_uds_broker
  934     1 ism      S     9280   2%   0% /usr/sbin/ismd -b QR22133GR000240
  849     1 root     S     9124   2%   0% firewall-app
 1045   959 root     S     8640   2%   0% icmpv6d
 1544   959 root     S     8572   2%   0% /usr/bin/selfhealing
 2022   959 root     S     7884   2%   0% dhclient -d -cf /tmp/etc/dhclient_extender.conf -pf /tmp/etc/dhclient_extender.pid -lf /opt/data/dhclient_extender.leases BR_LAN
 1415     1 root     S     7704   2%   0% {syslog-ng} supervising syslog-ng
 2117   959 root     S     7648   2%   0% /usr/sbin/lighttpd -f /etc/lighttpd/lighttpd.conf -D
17826  1021 root     S     6520   1%   0% hostapd -s /tmp/wl0.3_hapd.conf
17815  1021 root     S     6520   1%   0% hostapd -s /tmp/wl1_hapd.conf
17818  1021 root     S     6520   1%   0% hostapd -s /tmp/wl0.1_hapd.conf
23393 23379 root     S     5068   1%   0% -ash
    1     0 root     S     4940   1%   0% /sbin/init
  957     1 root     S     4940   1%   0% {hg6d_start} /bin/sh /usr/bin/hg6d_start
  437     1 root     S     4940   1%   0% /sbin/getty 115200 ttyAMA0
 6360 23393 root     R     4940   1%   0% top -bn1
18055  1021 root     S     4912   1%   0% hspotap
 1370   959 nobody   S     3288   1%   0% dnsmasq -k -u nobody -g ism --bogus-priv -i lo --bind-dynamic -c100 -r/tmp/dnsconf/relayresolv.conf --min-port=1024 -o --dns-retransmission-timeout=800 --do-retrans --hostsdir=/tmp/dnshosts/ --dynconf-server /tmp/dnsconf/dnsqueriesredirect.sgc --stop-dns-rebind --dynamic-dnsrebind=/tmp/dnsconf/dns_rebind.sgc
 3124  1021 root     S     2988   1%   0% acsd2 -F
17819  1021 root     S     2632   1%   0% eapd -F
23379 26013 root     S     2424   0%   0% dropbear -F -j -k -U root -p [192.168.1.89]:22 -P /var/run/dropbear.pid.pid..192.168.1.89
26013   959 root     S     2296   0%   0% dropbear -F -j -k -U root -p [192.168.1.89]:22 -P /var/run/dropbear.pid.pid..192.168.1.89
 1011   959 root     S     2004   0%   0% mcpd
 1154     2 root     SW       0   0%   0% [wl1-kthrd]
  816     2 root     SW       0   0%   0% [fc_timer]
  884     2 root     SW       0   0%   0% [bcmsw_rx]
   14     2 root     SW       0   0%   0% [ksoftirqd/1]
 1123     2 root     SW       0   0%   0% [dhd_watchdog_th]
    7     2 root     SW       0   0%   0% [rcu_preempt]
  871     2 root     SW       0   0%   0% [bcm_archer_us]
  815     2 root     SW       0   0%   0% [fc_evt]
  186     2 root     SW       0   0%   0% [skb_free_task]
  885     2 root     SW       0   0%   0% [bcmsw_recycle]
  872     2 root     SW       0   0%   0% [bcm_archer_wlan]
  274     2 root     SW       0   0%   0% [hwrng]
   10     2 root     SW       0   0%   0% [migration/0]
   13     2 root     SW       0   0%   0% [migration/1]
  390     2 root     SW       0   0%   0% [kworker/2:1]
  518     2 root     SW       0   0%   0% [ubi_bgt2d]
    3     2 root     SW       0   0%   0% [ksoftirqd/0]
  817     2 root     SW       0   0%   0% [bcmFlwStatsTask]
13973     2 root     SW       0   0%   0% [kworker/1:1]
24798     2 root     SW       0   0%   0% [kworker/0:1]
   17     2 root     SW       0   0%   0% [watchdog/2]
   11     2 root     SW       0   0%   0% [watchdog/0]
   12     2 root     SW       0   0%   0% [watchdog/1]
10094     2 root     SW       0   0%   0% [kworker/0:0]
18353     2 root     SW       0   0%   0% [kworker/u6:2]
23856     2 root     SW       0   0%   0% [kworker/u6:0]
    2     0 root     SW       0   0%   0% [kthreadd]
  461     2 root     SW       0   0%   0% [ubi_bgt1d]
  394     2 root     SW       0   0%   0% [ubi_bgt0d]
  415     2 root     SW<      0   0%   0% [kworker/0:1H]
  590     2 root     SW       0   0%   0% [ubifs_bgt2_1]
    5     2 root     SW<      0   0%   0% [kworker/0:0H]
    8     2 root     SW       0   0%   0% [rcu_sched]
    9     2 root     SW       0   0%   0% [rcu_bh]
   16     2 root     SW<      0   0%   0% [kworker/1:0H]
   18     2 root     SW       0   0%   0% [migration/2]
   19     2 root     SW       0   0%   0% [ksoftirqd/2]
   20     2 root     SW       0   0%   0% [kworker/2:0]
   21     2 root     SW<      0   0%   0% [kworker/2:0H]
   22     2 root     SW<      0   0%   0% [khelper]
   23     2 root     SW       0   0%   0% [kdevtmpfs]
   24     2 root     SW<      0   0%   0% [netns]
   27     2 root     SW<      0   0%   0% [perf]
  162     2 root     SW<      0   0%   0% [writeback]
  164     2 root     SW<      0   0%   0% [crypto]
  166     2 root     SW<      0   0%   0% [bioset]
  168     2 root     SW<      0   0%   0% [kblockd]
  187     2 root     SW<      0   0%   0% [linkwatch]
  200     2 root     SW<      0   0%   0% [mptcp_wq]
  201     2 root     SW<      0   0%   0% [rpciod]
  214     2 root     SWN      0   0%   0% [kswapd0]
  215     2 root     SW       0   0%   0% [fsnotify_mark]
  216     2 root     SW<      0   0%   0% [nfsiod]
  236     2 root     SW<      0   0%   0% [kthrotld]
  371     2 root     SW       0   0%   0% [bpm_monitor]
  373     2 root     SW<      0   0%   0% [ipv6_addrconf]
  387     2 root     SW<      0   0%   0% [deferwq]
  416     2 root     SW<      0   0%   0% [kworker/1:1H]
  886     2 root     SW       0   0%   0% [enet-kthrd]
 1102     2 root     SW<      0   0%   0% [cfg80211]
27267     2 root     SW       0   0%   0% [kworker/1:2]
"""
def test_parse_top_cmd():
    """_summary_
    """
    row = {}
    parse_top(OUTPUT_TOP_CMD, row)
    assert row["TOP_PROCESS_hg6d"] == 0
    assert row["TOP_PROCESS_swand"] == 0
