import os
import time
import argparse
import subprocess


def run_task(command, time_threshold=None):
    print('\nstart run:%s\n' % (command))
    delta_time = 0
    # task 1
    try_max = 3
    try_count = 0
    if time_threshold != None:
        while delta_time < time_threshold and try_count <= try_max:
            start_time = time.time()
            os.system(command)
            delta_time = time.time() - start_time
            print('\n\n{} finished ,detal time : {} retry: {}'.format(command, delta_time, try_count))
            time.sleep(2)
            try_count += 1
    else:
        exit_code = subprocess.call(command, shell=True)
        if exit_code != 0: exit(exit_code)
        time.sleep(2)

class Task(object):

    def __init__(self, fast_test=False, tag ='unknown_tag'):
        self.fast_test = fast_test
        self.tag=tag

    def train_rpn(self):

        run_task('python train.py -t "top_view_rpn" -i 600 '
                 '-n %s' % (self.tag))
        for i in range(20):
            run_task('python train.py -w "top_view_rpn" -t "top_view_rpn" -i 600 '
                     ' -n %s -c True' %(self.tag))
            run_task('python tracking.py -n %s' % (self.tag))



    def train_img_and_fusion(self):

        iter = lambda i:  i if self.fast_test==False else 1

        run_task('python train.py -w "top_view_rpn" -t "image_feature,fusion" -i %d '
                 '-n %s' % (iter(700), self.tag))

        for i in range(iter(5)):
            run_task('python train.py -w "top_view_rpn,image_feature,fusion" -t "image_feature,fusion" -i %d '
                     ' -n %s -c True' %(iter(4000), tag))
            run_task('python tracking.py -n %s_%d -w "%s" -t "%s"' % (tag,i,tag,self.fast_test))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tracking')
    parser.add_argument('-n', '--tag', type=str, nargs='?', default='unknown_tag',
                        help='set log tag')
    parser.add_argument('-t', '--fast_test', type=bool, nargs='?', default=False,
                        help='fast test mode')
    args = parser.parse_args()

    print('\n\n{}\n\n'.format(args))
    tag = args.tag
    if tag == 'unknow_tag':
        # tag = input('Enter log tag : ')
        print('\nSet log tag :"%s" ok !!\n' %tag)

    Task(tag=tag, fast_test=args.fast_test).train_img_and_fusion()