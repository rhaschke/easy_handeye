#!/usr/bin/env python

import rospy
import std_srvs
from std_srvs import srv
from handeyecalibration.handeye_client import HandeyeClient


# for reading single character without hitting RETURN (unless it's ipython!)
def getchar():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


class HandeyeCalibrationCommander:
    def __init__(self):
        self.client = HandeyeClient()

    def _edit_menu(self):
        sample_list = self.client.get_sample_list()
        sample_to_delete = None
        while sample_to_delete != '':
            prompt_str = 'Press a number and ENTER to delete the respective sample, or ENTER to continue:\n'
            for i in range(len(sample_list)):
                prompt_str += str(i + 1) + ' ' + str(sample_list[i]) + '\n'
            sample_to_delete = raw_input(prompt_str)
            if sample_to_delete.isdigit():
                self.client.remove_sample(sample_to_delete)

    def _save_menu(self):
        print('Press c to compute the calibration or ENTER to continue\n')
        i = getchar()
        if i == 'c':
            cal = self.compute_calibration_proxy()
            print(cal)
        print('Press q+ENTER to quit or ENTER to continue\n')
        i = getchar()
        if i == 'q':
            quit()

    def _interactive_menu(self):
        self._edit_menu()
        self._save_menu()

    def spin_interactive(self):
        while not rospy.is_shutdown():
            self._interactive_menu()


def main():
    rospy.init_node('handeyecalibration')
    while rospy.get_time() == 0.0:
        pass

    cmder = HandeyeCalibrationCommander()
    cmder.spin_interactive()


if __name__ == '__main__':
    main()
