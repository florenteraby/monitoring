import pytest
import logging
from monitor import parse_process_VMZ

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
    row = {}
    parse_process_VMZ(OUTPUT_PSAUX_M, row, supply_logger)
    assert row["VMZ_HG6D"] == 120000000
    assert row["VMZ_WSHD"] == 10196
    assert row["VMZ_WSTD"] == 10188
    assert row["VMZ_DHCLIENT"] == 5204
    assert row["VMZ_DHRELAY"] == 4944
    assert row["VMZ_ISMD"] == 7888
    assert row["VMZ_DNSMASQ"] == 3420
