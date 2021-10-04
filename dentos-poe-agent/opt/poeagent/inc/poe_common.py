'''
Copyright 2021 Delta Electronic Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import os
import sys
import syslog
import fcntl

# POE Driver Attributes
TOTAL_PORTS   = "total_ports"
TOTAL_POWER   = "total_power"
POWER_LIMIT   = "power_limit"
POWER_CONSUMP = "power_consump"
POWER_AVAIL   = "power_avail"
POWER_BANK    = "power_bank"
POWER_SRC     = "power_src"
STATUS        = "status"
PRIORITY      = "priority"
PORT_ID       = "port_id"
MAX_SD_VOLT   = "max_sd_volt"
MIN_SD_VOLT   = "min_sd_volt"
PPL           = "ppl"
TPPL          = "tppl"
ENDIS         = "enDis"
CPU_STATUS1   = "cpu_status1"
CPU_STATUS2   = "cpu_status2"
FAC_DEFAULT   = "fac_def"
GIE           = "gen_intl_err"
PRIV_LABEL    = "priv_label"
USER_BYTE     = "user_byte"
DEVICE_FAIL   = "device_fail"
TEMP_DISCO    = "temp_disc"
TEMP_ALARM    = "temp_alarm"
INTR_REG      = "intr_reg"
PROTOCOL      = "protocol"
CLASS         = "class"
VOLTAGE       = "voltage"
CURRENT       = "current"
CSNUM         = "poe_dev_addr_num"
TEMP          = "temperature"
LATCH         = "latch"
EN_4PAIR      = "enable_4pair"
PM1           = "pm1"
PM2           = "pm2"
PM3           = "pm3"
SW_VERSION    = "sw_version"
PROD_NUM      = "prod_num"

# POE Configuration Attributes
GEN_INFO       = "GENERAL_INFORMATION"
TIMESTAMP      = "TIMESTAMP"
SYS_INFO       = "SYSTEM_INFORMATION"
PORT_CONFIGS   = "PORTS_CONFIGURATIONS"
PORT_INFO      = "PORT_INFORMATION"
INDV_MASKS     = "INDV_MASKS"
VERSIONS       = "VERSIONS"
PLATFORM       = "platform"
POE_AGT_VER    = "poe_agent_version"
POE_CFG_VER    = "poe_config_version"
CFG_SERIAL_NUM = "file_serial_number"
LAST_SAVE_TIME = "file_save_time"
LAST_SET_TIME  = "last_poe_set_time"

# IPC EVENT
POE_SET_EVT    = "/tmp/poe_set_event"
POECLI_SET     = "poecli_set"

# POE Access Exclusive Lock
POE_ACCESS_LOCK = "/tmp/poe_access.lock"

class PoeLog(object):
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode

    def emerg(self, msg):
        self._record(syslog.LOG_EMERG, "EMERG: %s" % msg)

    def alert(self, msg):
        self._record(syslog.LOG_ALERT, "ALERT: %s" % msg)

    def crit(self, msg):
        self._record(syslog.LOG_CRIT, "CRIT: %s" % msg)

    def err(self, msg):
        self._record(syslog.LOG_ERR, "ERR: %s" % msg)

    def warn(self, msg):
        self._record(syslog.LOG_WARNING, "WARN: %s" % msg)

    def notice(self, msg):
        self._record(syslog.LOG_NOTICE, "NOTICE: %s" % msg)

    def info(self, msg):
        self._record(syslog.LOG_INFO, "INFO: %s" % msg)

    def dbg(self, msg):
        self._record(syslog.LOG_DEBUG, "DBG: %s" % msg)

    def _record(self, priority, msg):
        syslog.syslog(priority, msg)
        if self.debug_mode == True:
            print(msg)

def PoeAccessExclusiveLock(func):
    def wrap_cmd(*args, **kwargs):
        try:
            fd = open(POE_ACCESS_LOCK, 'r')
        except IOError:
            fd = open(POE_ACCESS_LOCK, 'wb')

        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            res = func(*args, **kwargs)
        except IOError:
            pass
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
            return res
    return wrap_cmd
