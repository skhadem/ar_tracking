#!/usr/bin/env python
import rospy

import tf

from ar_track_alvar_msgs.msg import AlvarMarkers
listener = tf.TransformListener()
def handle_ar_pos(msg):
    print("got it")
    avg_x = 0
    avg_y = 0
    avg_z = 0

    avg_ox = 0
    avg_oy = 0
    avg_oz = 0
    avg_ow = 0

    marker_count = 0
    for marker in msg.markers:
        x = marker.pose.pose.position.x
        y = marker.pose.pose.position.y
        z = marker.pose.pose.position.z

        avg_x += x
        avg_y += y
        avg_z += z

        ox = marker.pose.pose.orientation.x
        oy = marker.pose.pose.orientation.y
        oz = marker.pose.pose.orientation.z
        ow = marker.pose.pose.orientation.w

        avg_ox += ox
        avg_oy += oy
        avg_oz += oz
        avg_ow += ow

        marker_count += 1

    avg_x = avg_x/marker_count
    avg_y = avg_y/marker_count
    avg_z = avg_z/marker_count

    avg_ox = avg_ox/marker_count
    avg_oy = avg_oy/marker_count
    avg_oz = avg_oz/marker_count
    avg_ow = avg_ow/marker_count

    # print(ox)
    # print(avg_ox)

    br = tf.TransformBroadcaster()

    try:
        (trans, rot) = listener.lookupTransform('marker_bundle', 'world', rospy.Time(0))
        br.sendTransform((avg_x - trans[0], avg_y - trans[1], avg_z - trans[2]),
                    (ox,oy,oz,ow),
                    rospy.Time.now(),
                    "occam",
                    "world")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    rospy.init_node('occam_world_transform')

    try:
        rospy.Subscriber('/ar_pose_marker', AlvarMarkers, handle_ar_pos)
    except Exception as e:
        print(e)
    rospy.spin()
# if __name__ == '__main__':
#     rospy.init_node('occam_world_transform')
#
#     listener = tf.TransformListener()
#     br = tf.TransformBroadcaster()
#
#     rate = rospy.Rate(10.0)
#     while not rospy.is_shutdown():
#         try:
#             (trans,rot) = listener.lookupTransform('/ar_marker_0', '/occam', rospy.Time(0))
#             br.sendTransform(trans, rot, rospy.Time.now(), "occam_copy", "world_copy")
#             print("got it")
#             print(trans)
#         except Exception as e:
#             print(e)
#             continue
#
#         rate.sleep()
