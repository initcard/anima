# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Anima Istanbul
#
# This module is part of anima-tools and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
import os
import unittest
import pymel

from edl import List, Event

from anima.previs import (SequencerExtension, Sequence, Media, Video, Track,
                          Clip, File)


class SequenceTestCase(unittest.TestCase):
    """tests the anima.previs.Sequence class
    """

    def test_to_xml_method_is_working_properly(self):
        """testing if the to xml method is working properly
        """
        s = Sequence()
        s.duration = 109.0
        s.name = 'previs_edit_v001'
        s.ntsc = False
        s.timebase = 24
        s.timecode = '00:00:00:00'

        m = Media()
        s.media = m

        v = Video()
        v.width = 1024
        v.height = 778
        m.video = v

        t = Track()
        t.enabled = True
        t.locked = False

        v.tracks.append(t)

        # clip 1
        f = File()
        f.duration = 34.0
        f.name = 'shot2'
        f.pathurl = 'file:///home/eoyilmaz/maya/projects/default/data/shot2.mov'

        c = Clip()
        c.id = 'shot2'
        c.start = 1.0
        c.end = 35.0
        c.name = 'shot2'
        c.enabled = True
        c.duration = 34.0
        c.in_ = 0.0
        c.out = 34.0
        c.file = f

        t.clips.append(c)

        # clip 2
        f = File()
        f.duration = 30.0
        f.name = 'shot'
        f.pathurl = 'file:///home/eoyilmaz/maya/projects/default/data/shot.mov'

        c = Clip()
        c.id = 'shot'
        c.start = 35.0
        c.end = 65.0
        c.name = 'shot'
        c.enabled = True
        c.duration = 30.0
        c.in_ = 0.0
        c.out = 30.0
        c.file = f

        t.clips.append(c)

        # clip 3
        f = File()
        f.duration = 45.0
        f.name = 'shot1'
        f.pathurl = 'file:///home/eoyilmaz/maya/projects/default/data/shot1.mov'

        c = Clip()
        c.id = 'shot1'
        c.start = 65.0
        c.end = 110.0
        c.name = 'shot1'
        c.enabled = True
        c.duration = 45.0
        c.in_ = 0.0
        c.out = 45.0
        c.file = f

        t.clips.append(c)

        expected_xml = \
            """<sequence>
  <duration>109.0</duration>
  <name>previs_edit_v001</name>
  <rate>
    <ntsc>FALSE</ntsc>
    <timebase>24</timebase>
  </rate>
  <timecode>
    <string>00:00:00:00</string>
  </timecode>
  <media>
    <video>
      <format>
        <samplecharacteristics>
          <width>1024</width>
          <height>778</height>
        </samplecharacteristics>
      </format>
      <track>
        <locked>FALSE</locked>
        <enabled>TRUE</enabled>
        <clipitem id="shot2">
          <end>35.0</end>
          <name>shot2</name>
          <enabled>True</enabled>
          <start>1.0</start>
          <in>0.0</in>
          <duration>34.0</duration>
          <out>34.0</out>
          <file>
            <duration>34.0</duration>
            <name>shot2</name>
            <pathurl>file:///home/eoyilmaz/maya/projects/default/data/shot2.mov</pathurl>
          </file>
        </clipitem>
        <clipitem id="shot">
          <end>65.0</end>
          <name>shot</name>
          <enabled>True</enabled>
          <start>35.0</start>
          <in>0.0</in>
          <duration>30.0</duration>
          <out>30.0</out>
          <file>
            <duration>30.0</duration>
            <name>shot</name>
            <pathurl>file:///home/eoyilmaz/maya/projects/default/data/shot.mov</pathurl>
          </file>
        </clipitem>
        <clipitem id="shot1">
          <end>110.0</end>
          <name>shot1</name>
          <enabled>True</enabled>
          <start>65.0</start>
          <in>0.0</in>
          <duration>45.0</duration>
          <out>45.0</out>
          <file>
            <duration>45.0</duration>
            <name>shot1</name>
            <pathurl>file:///home/eoyilmaz/maya/projects/default/data/shot1.mov</pathurl>
          </file>
        </clipitem>
      </track>
    </video>
  </media>
</sequence>"""

        self.assertEqual(
            expected_xml,
            s.to_xml()
        )

    def test_from_xml_method_is_working_properly(self):
        """testing if the from_xml method will fill object attributes from the
        given xml node
        """
        from xml.etree import ElementTree
        sequence_node = ElementTree.Element('sequence')
        duration_node = ElementTree.SubElement(sequence_node, 'duration')
        duration_node.text = '109.0'
        name_node = ElementTree.SubElement(sequence_node, 'name')
        name_node.text = 'previs_edit_v001'
        rate_node = ElementTree.SubElement(sequence_node, 'rate')
        ntsc_node = ElementTree.SubElement(rate_node, 'ntsc')
        ntsc_node.text = 'FALSE'
        timebase_node = ElementTree.SubElement(rate_node, 'timebase')
        timebase_node.text = '24'
        timecode_node = ElementTree.SubElement(sequence_node, 'timecode')
        string_node = ElementTree.SubElement(timecode_node, 'string')
        string_node.text = '00:00:00:00'

        media_node = ElementTree.SubElement(sequence_node, 'media')

        video_node = ElementTree.SubElement(media_node, 'video')
        format_node = ElementTree.SubElement(video_node, 'format')
        sc_node = ElementTree.SubElement(format_node, 'samplecharacteristics')
        width_node = ElementTree.SubElement(sc_node, 'width')
        width_node.text = 1024
        height_node = ElementTree.SubElement(sc_node, 'height')
        height_node.text = 778

        track_node = ElementTree.SubElement(video_node, 'track')
        locked_node = ElementTree.SubElement(track_node, 'locked')
        locked_node.text = 'FALSE'
        enabled_node = ElementTree.SubElement(track_node, 'enabled')
        enabled_node.text = 'TRUE'

        # clip1
        clip_node = ElementTree.SubElement(track_node, 'clipitem',
                                           attrib={'id': 'shot2'})
        end_node = ElementTree.SubElement(clip_node, 'end')
        end_node.text = '35.0'
        name_node = ElementTree.SubElement(clip_node, 'name')
        name_node.text = 'shot2'
        enabled_node = ElementTree.SubElement(clip_node, 'enabled')
        enabled_node.text = 'True'
        start_node = ElementTree.SubElement(clip_node, 'start')
        start_node.text = '1.0'
        in_node = ElementTree.SubElement(clip_node, 'in')
        in_node.text = '0.0'
        duration_node = ElementTree.SubElement(clip_node, 'duration')
        duration_node.text = '34.0'
        out_node = ElementTree.SubElement(clip_node, 'out')
        out_node.text = '34.0'

        file_node = ElementTree.SubElement(clip_node, 'file')
        duration_node = ElementTree.SubElement(file_node, 'duration')
        duration_node.text = '34.0'
        name_node = ElementTree.SubElement(file_node, 'name')
        name_node.text = 'shot2'
        pathurl_node = ElementTree.SubElement(file_node, 'pathurl')

        pathurl = 'file:///home/eoyilmaz/maya/projects/default/data/shot2.mov'
        pathurl_node.text = pathurl

        # clip2
        clip_node = ElementTree.SubElement(track_node, 'clipitem',
                                           attrib={'id': 'shot'})
        end_node = ElementTree.SubElement(clip_node, 'end')
        end_node.text = '65.0'
        name_node = ElementTree.SubElement(clip_node, 'name')
        name_node.text = 'shot'
        enabled_node = ElementTree.SubElement(clip_node, 'enabled')
        enabled_node.text = 'True'
        start_node = ElementTree.SubElement(clip_node, 'start')
        start_node.text = '35.0'
        in_node = ElementTree.SubElement(clip_node, 'in')
        in_node.text = '0.0'
        duration_node = ElementTree.SubElement(clip_node, 'duration')
        duration_node.text = '30.0'
        out_node = ElementTree.SubElement(clip_node, 'out')
        out_node.text = '30.0'

        file_node = ElementTree.SubElement(clip_node, 'file')
        duration_node = ElementTree.SubElement(file_node, 'duration')
        duration_node.text = '30.0'
        name_node = ElementTree.SubElement(file_node, 'name')
        name_node.text = 'shot'
        pathurl_node = ElementTree.SubElement(file_node, 'pathurl')

        pathurl = 'file:///home/eoyilmaz/maya/projects/default/data/shot.mov'
        pathurl_node.text = pathurl

        # clip3
        clip_node = ElementTree.SubElement(track_node, 'clipitem',
                                           attrib={'id': 'shot1'})
        end_node = ElementTree.SubElement(clip_node, 'end')
        end_node.text = '110.0'
        name_node = ElementTree.SubElement(clip_node, 'name')
        name_node.text = 'shot1'
        enabled_node = ElementTree.SubElement(clip_node, 'enabled')
        enabled_node.text = 'True'
        start_node = ElementTree.SubElement(clip_node, 'start')
        start_node.text = '65.0'
        in_node = ElementTree.SubElement(clip_node, 'in')
        in_node.text = '0.0'
        duration_node = ElementTree.SubElement(clip_node, 'duration')
        duration_node.text = '45.0'
        out_node = ElementTree.SubElement(clip_node, 'out')
        out_node.text = '45.0'

        file_node = ElementTree.SubElement(clip_node, 'file')
        duration_node = ElementTree.SubElement(file_node, 'duration')
        duration_node.text = '45.0'
        name_node = ElementTree.SubElement(file_node, 'name')
        name_node.text = 'shot1'
        pathurl_node = ElementTree.SubElement(file_node, 'pathurl')

        pathurl = 'file:///home/eoyilmaz/maya/projects/default/data/shot1.mov'
        pathurl_node.text = pathurl

        s = Sequence()
        s.from_xml(sequence_node)
        self.assertEqual(109.0, s.duration)
        self.assertEqual('previs_edit_v001', s.name)
        self.assertEqual(False, s.ntsc)
        self.assertEqual('24', s.timebase)
        self.assertEqual('00:00:00:00', s.timecode)

        m = s.media

        v = m.video
        self.assertEqual(1024, v.width)
        self.assertEqual(778, v.height)

        t = v.tracks[0]
        self.assertEqual(False, t.locked)
        self.assertEqual(True, t.enabled)

        # clip1
        c = t.clips[0]
        self.assertEqual(35.0, c.end)
        self.assertEqual('shot2', c.name)
        self.assertEqual(True, c.enabled)
        self.assertEqual(1.0, c.start)
        self.assertEqual(0.0, c.in_)
        self.assertEqual(34.0, c.duration)
        self.assertEqual(34.0, c.out)

        f = c.file
        self.assertEqual(34.0, f.duration)
        self.assertEqual('shot2', f.name)
        self.assertEqual(
            'file:///home/eoyilmaz/maya/projects/default/data/shot2.mov',
            f.pathurl
        )

        # clip2
        c = t.clips[1]
        self.assertEqual(65.0, c.end)
        self.assertEqual('shot', c.name)
        self.assertEqual(True, c.enabled)
        self.assertEqual(35.0, c.start)
        self.assertEqual(0.0, c.in_)
        self.assertEqual(30.0, c.duration)
        self.assertEqual(30.0, c.out)

        f = c.file
        self.assertEqual(30.0, f.duration)
        self.assertEqual('shot', f.name)
        self.assertEqual(
            'file:///home/eoyilmaz/maya/projects/default/data/shot.mov',
            f.pathurl
        )

        # clip3
        c = t.clips[2]
        self.assertEqual(110.0, c.end)
        self.assertEqual('shot1', c.name)
        self.assertEqual(True, c.enabled)
        self.assertEqual(65.0, c.start)
        self.assertEqual(0.0, c.in_)
        self.assertEqual(45.0, c.duration)
        self.assertEqual(45.0, c.out)

        f = c.file
        self.assertEqual(45.0, f.duration)
        self.assertEqual('shot1', f.name)
        self.assertEqual(
            'file:///home/eoyilmaz/maya/projects/default/data/shot1.mov',
            f.pathurl
        )

    def test_to_edl_will_raise_RuntimeError_if_no_Media_instance_presents(self):
        """testing if a RuntimeError will be raised when there is no Media
        instance present in Sequence
        """
        s = Sequence()
        with self.assertRaises(RuntimeError) as cm:
            s.to_edl()

        self.assertEqual(
            'Can not run Sequence.to_edl() without a Media instance, please '
            'add a Media instance to this Sequence instance.',
            cm.exception.message
        )

    def test_to_edl_method_will_return_a_List_instance(self):
        """testing if to_edl method will return an edl.List instance
        """
        s = Sequence()
        m = Media()
        s.media = m

        result = s.to_edl()
        self.assertIsInstance(result, List)

    def test_to_edl_method_is_working_properly(self):
        """testing if the to_edl method will output a proper edl.List object
        """
        # create Sequence instance from XML
        sm = pymel.core.PyNode('sequenceManager1')
        sm.set_version('v001')
        xml_path = os.path.abspath('./test_data/test_v001.xml')
        sm.from_xml(xml_path)

        sequence = sm.generate_sequence_structure()

        edl_list = sm.to_edl()
        self.assertIsInstance(edl_list, List)

        self.assertEqual(
            sequence.name,
            edl_list.title
        )

        # events should be clips
        self.assertEqual(3, len(edl_list.events))

        e1 = edl_list.events[0]
        e2 = edl_list.events[1]
        e3 = edl_list.events[2]

        self.assertIsInstance(e1, Event)
        self.assertIsInstance(e2, Event)
        self.assertIsInstance(e3, Event)

        # check clips
        clips = sequence.media.video.tracks[0].clips
        self.assertIsInstance(clips[0], Clip)

        self.assertEqual('000001', e1.num)
        self.assertEqual('SEQ001_HSNI_003_0010_v001', e1.clip_name)
        self.assertEqual('SEQ001_HSNI_003_0010_v001', e1.reel)
        self.assertEqual('V', e1.track)
        self.assertEqual('C', e1.tr_code)
        self.assertEqual('00:00:00:00', e1.src_start_tc)
        self.assertEqual('00:00:01:10', e1.src_end_tc)
        self.assertEqual('00:00:00:01', e1.rec_start_tc)
        self.assertEqual('00:00:01:11', e1.rec_end_tc)
        self.assertEqual(
            '* FROM CLIP NAME: SEQ001_HSNI_003_0010_v001',
            e1.comments[0]
        )
        self.assertEqual('/tmp/SEQ001_HSNI_003_0010_v001.mov', e1.source_file)
        self.assertEqual(
            '* SOURCE FILE: /tmp/SEQ001_HSNI_003_0010_v001.mov', e1.comments[1]
        )

        self.assertEqual('000002', e2.num)
        self.assertEqual('SEQ001_HSNI_003_0020_v001', e2.clip_name)
        self.assertEqual('SEQ001_HSNI_003_0020_v001', e2.reel)
        self.assertEqual('V', e2.track)
        self.assertEqual('C', e2.tr_code)
        self.assertEqual('00:00:00:00', e2.src_start_tc)
        self.assertEqual('00:00:01:07', e2.src_end_tc)
        self.assertEqual('00:00:01:11', e2.rec_start_tc)
        self.assertEqual('00:00:02:18', e2.rec_end_tc)
        self.assertEqual('/tmp/SEQ001_HSNI_003_0020_v001.mov',
                         e2.source_file)
        self.assertEqual(
            '* FROM CLIP NAME: SEQ001_HSNI_003_0020_v001',
            e2.comments[0]
        )
        self.assertEqual(
            '* SOURCE FILE: /tmp/SEQ001_HSNI_003_0020_v001.mov',
            e2.comments[1]
        )

        self.assertEqual('000003', e3.num)
        self.assertEqual('SEQ001_HSNI_003_0030_v001', e3.clip_name)
        self.assertEqual('SEQ001_HSNI_003_0030_v001', e3.reel)
        self.assertEqual('V', e3.track)
        self.assertEqual('C', e3.tr_code)
        self.assertEqual('00:00:00:00', e3.src_start_tc)
        self.assertEqual('00:00:01:22', e3.src_end_tc)
        self.assertEqual('00:00:02:18', e3.rec_start_tc)
        self.assertEqual('00:00:04:16', e3.rec_end_tc)
        self.assertEqual('/tmp/SEQ001_HSNI_003_0030_v001.mov',
                         e3.source_file)
        self.assertEqual(
            '* FROM CLIP NAME: SEQ001_HSNI_003_0030_v001',
            e3.comments[0]
        )
        self.assertEqual(
            '* SOURCE FILE: /tmp/SEQ001_HSNI_003_0030_v001.mov',
            e3.comments[1]
        )

    def test_from_edl_method_is_working_properly(self):
        """testing if the from_edl method will return an anima.previs.Sequence
        instance with proper hierarchy
        """
        # first supply an edl
        from edl import Parser
        p = Parser('24')
        edl_path = os.path.abspath('./test_data/test_v001.edl')

        with open(edl_path) as f:
            edl_list = p.parse(f)

        s = Sequence(timebase='24')
        s.from_edl(edl_list)

        self.assertEqual('SEQ001_HSNI_003', s.name)

        self.assertEqual(111.0, s.duration)
        self.assertEqual('24', s.timebase)
        self.assertEqual('00:00:00:00', s.timecode)

        m = s.media
        self.assertIsInstance(m, Media)

        v = m.video
        self.assertIsInstance(v, Video)

        t = v.tracks[0]
        self.assertEqual(False, t.locked)
        self.assertEqual(True, t.enabled)

        clips = t.clips
        self.assertEqual(3, len(clips))

        clip1 = clips[0]
        clip2 = clips[1]
        clip3 = clips[2]

        self.assertIsInstance(clip1, Clip)
        self.assertIsInstance(clip2, Clip)
        self.assertIsInstance(clip3, Clip)

        # clip1
        self.assertEqual(44.0, clip1.duration)
        self.assertEqual(True, clip1.enabled)
        self.assertEqual(35.0, clip1.end)
        self.assertEqual('SEQ001_HSNI_003_0010_v001', clip1.id)
        self.assertEqual(10.0, clip1.in_)
        self.assertEqual('SEQ001_HSNI_003_0010_v001', clip1.name)
        self.assertEqual(44.0, clip1.out)
        self.assertEqual(1.0, clip1.start)
        self.assertEqual('Video', clip1.type)

        f = clip1.file
        self.assertIsInstance(f, File)
        self.assertEqual(44.0, f.duration)
        self.assertEqual('SEQ001_HSNI_003_0010_v001', f.name)
        self.assertEqual(
            'file:///tmp/SEQ001_HSNI_003_0010_v001.mov',
            f.pathurl
        )

        # clip2
        self.assertEqual(41.0, clip2.duration)
        self.assertEqual(True, clip2.enabled)
        self.assertEqual(66.0, clip2.end)
        self.assertEqual('SEQ001_HSNI_003_0020_v001', clip2.id)
        self.assertEqual(10.0, clip2.in_)
        self.assertEqual('SEQ001_HSNI_003_0020_v001', clip2.name)
        self.assertEqual(41.0, clip2.out)
        self.assertEqual(35.0, clip2.start)
        self.assertEqual('Video', clip2.type)

        f = clip2.file
        self.assertIsInstance(f, File)
        self.assertEqual(41.0, f.duration)
        self.assertEqual('SEQ001_HSNI_003_0020_v001', f.name)
        self.assertEqual(
            'file:///tmp/SEQ001_HSNI_003_0020_v001.mov',
            f.pathurl
        )

        # clip3
        self.assertEqual(56.0, clip3.duration)
        self.assertEqual(True, clip3.enabled)
        self.assertEqual(112.0, clip3.end)
        self.assertEqual('SEQ001_HSNI_003_0030_v001', clip3.id)
        self.assertEqual(10.0, clip3.in_)
        self.assertEqual('SEQ001_HSNI_003_0030_v001', clip3.name)
        self.assertEqual(56.0, clip3.out)
        self.assertEqual(66.0, clip3.start)
        self.assertEqual('Video', clip3.type)

        f = clip3.file
        self.assertIsInstance(f, File)
        self.assertEqual(56.0, f.duration)
        self.assertEqual('SEQ001_HSNI_003_0030_v001', f.name)
        self.assertEqual(
            'file:///tmp/SEQ001_HSNI_003_0030_v001.mov',
            f.pathurl
        )

    def test_from_edl_method_is_working_properly_with_negative_timecodes(self):
        """testing if the from_edl method will return an anima.previs.Sequence
        instance with proper hierarchy event with clips that has negative
        timecode values (timecodes with in point is bigger than out point and
        around 23:59:59:XX as a result)
        """
        # first supply an edl
        from edl import Parser
        p = Parser('24')
        edl_path = os.path.abspath('./test_data/test_v003.edl')

        with open(edl_path) as f:
            edl_list = p.parse(f)

        s = Sequence(timebase='24')
        s.from_edl(edl_list)

        self.assertEqual('SEQ001_HSNI_003', s.name)

        self.assertEqual(248.0, s.duration)
        self.assertEqual('24', s.timebase)
        self.assertEqual('00:00:00:00', s.timecode)

        m = s.media
        self.assertIsInstance(m, Media)

        v = m.video
        self.assertIsInstance(v, Video)

        t = v.tracks[0]
        self.assertEqual(False, t.locked)
        self.assertEqual(True, t.enabled)

        clips = t.clips
        self.assertEqual(3, len(clips))

        clip1 = clips[0]
        clip2 = clips[1]
        clip3 = clips[2]

        self.assertIsInstance(clip1, Clip)
        self.assertIsInstance(clip2, Clip)
        self.assertIsInstance(clip3, Clip)

        # clip1
        self.assertEqual(191.0, clip1.duration)
        self.assertEqual(True, clip1.enabled)
        self.assertEqual(153.0, clip1.end)
        self.assertEqual('SEQ001_HSNI_003_0010_v001', clip1.id)
        self.assertEqual(15.0, clip1.in_)
        self.assertEqual('SEQ001_HSNI_003_0010_v001', clip1.name)
        self.assertEqual(191.0, clip1.out)
        self.assertEqual(-24, clip1.start)
        self.assertEqual('Video', clip1.type)

        f = clip1.file
        self.assertIsInstance(f, File)
        self.assertEqual(191.0, f.duration)
        self.assertEqual('SEQ001_HSNI_003_0010_v001', f.name)
        self.assertEqual(
            'file:///tmp/SEQ001_HSNI_003_0010_v001.mov',
            f.pathurl
        )

        # clip2
        self.assertEqual(100, clip2.duration)
        self.assertEqual(True, clip2.enabled)
        self.assertEqual(208, clip2.end)
        self.assertEqual('SEQ001_HSNI_003_0020_v001', clip2.id)
        self.assertEqual(45.0, clip2.in_)
        self.assertEqual('SEQ001_HSNI_003_0020_v001', clip2.name)
        self.assertEqual(100.0, clip2.out)
        self.assertEqual(153.0, clip2.start)
        self.assertEqual('Video', clip2.type)

        f = clip2.file
        self.assertIsInstance(f, File)
        self.assertEqual(100.0, f.duration)
        self.assertEqual('SEQ001_HSNI_003_0020_v001', f.name)
        self.assertEqual(
            'file:///tmp/SEQ001_HSNI_003_0020_v001.mov',
            f.pathurl
        )

        # clip3
        self.assertEqual(1.0, clip3.duration)
        self.assertEqual(True, clip3.enabled)
        self.assertEqual(224.0, clip3.end)
        self.assertEqual('SEQ001_HSNI_003_0030_v001', clip3.id)
        self.assertEqual(0.0, clip3.in_)
        self.assertEqual('SEQ001_HSNI_003_0030_v001', clip3.name)
        self.assertEqual(1.0, clip3.out)
        self.assertEqual(208.0, clip3.start)
        self.assertEqual('Video', clip3.type)

        f = clip3.file
        self.assertIsInstance(f, File)
        self.assertEqual(1.0, f.duration)
        self.assertEqual('SEQ001_HSNI_003_0030_v001', f.name)
        self.assertEqual(
            'file:///tmp/SEQ001_HSNI_003_0030_v001.mov',
            f.pathurl
        )

    def test_to_metafuze_xml_is_working_properly(self):
        """testing if to_metafuze_xml method is working properly
        """
        s = Sequence()
        s.duration = 109.0
        s.name = 'SEQ001_HSNI_003'
        s.ntsc = False
        s.timebase = 24
        s.timecode = '00:00:00:00'

        m = Media()
        s.media = m

        v = Video()
        v.width = 1024
        v.height = 778
        m.video = v

        t = Track()
        t.enabled = True
        t.locked = False

        v.tracks.append(t)

        # clip 1
        f = File()
        f.duration = 34.0
        f.name = 'SEQ001_HSNI_003_0010_v001'
        f.pathurl = 'file:///tmp/SEQ001_HSNI_003_0010_v001.mov'

        c = Clip()
        c.id = '0010'
        c.start = 1.0
        c.end = 35.0
        c.name = 'SEQ001_HSNI_003_0010_v001'
        c.enabled = True
        c.duration = 34.0
        c.in_ = 0.0
        c.out = 34.0
        c.file = f

        t.clips.append(c)

        # clip 2
        f = File()
        f.duration = 30.0
        f.name = 'SEQ001_HSNI_003_0020_v001'
        f.pathurl = 'file:///tmp/SEQ001_HSNI_003_0020_v001.mov'

        c = Clip()
        c.id = '0020'
        c.start = 35.0
        c.end = 65.0
        c.name = 'SEQ001_HSNI_003_0020_v001'
        c.enabled = True
        c.duration = 30.0
        c.in_ = 0.0
        c.out = 30.0
        c.file = f

        t.clips.append(c)

        # clip 3
        f = File()
        f.duration = 45.0
        f.name = 'SEQ001_HSNI_003_0030_v001'
        f.pathurl = 'file:///tmp/SEQ001_HSNI_003_0030_v001.mov'

        c = Clip()
        c.id = '0030'
        c.start = 65.0
        c.end = 110.0
        c.name = 'SEQ001_HSNI_003_0030_v001'
        c.enabled = True
        c.duration = 45.0
        c.in_ = 0.0
        c.out = 45.0
        c.file = f

        t.clips.append(c)

        expected_xmls = [
            """<?xml version='1.0' encoding='UTF-8'?>
<MetaFuze_BatchTranscode xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="MetaFuzeBatchTranscode.xsd">
   <Configuration>
      <Local>8</Local>
      <Remote>8</Remote>
   </Configuration>
   <Group>
      <FileList>
         <File>/tmp/SEQ001_HSNI_003_0010_v001.mov</File>
      </FileList>
      <Transcode>
         <Version>1.0</Version>
         <File>/tmp/SEQ001_HSNI_003_0010_v001.mxf</File>
         <ClipName>SEQ001_HSNI_003_0010_v001</ClipName>
         <ProjectName>SEQ001_HSNI_003</ProjectName>
         <TapeName>SEQ001_HSNI_003_0010_v001</TapeName>
         <TC_Start>00:00:00:00</TC_Start>
         <DropFrame>false</DropFrame>
         <EdgeTC>** TimeCode N/A **</EdgeTC>
         <FilmType>35.4</FilmType>
         <KN_Start>AAAAAAAA-0000+00</KN_Start>
         <Frames>33</Frames>
         <Width>1024</Width>
         <Height>778</Height>
         <PixelRatio>1.0000</PixelRatio>
         <UseFilmInfo>false</UseFilmInfo>
         <UseTapeInfo>true</UseTapeInfo>
         <AudioChannelCount>0</AudioChannelCount>
         <UseMXFAudio>false</UseMXFAudio>
         <UseWAVAudio>false</UseWAVAudio>
         <SrcBitsPerChannel>8</SrcBitsPerChannel>
         <OutputPreset>DNxHD 36</OutputPreset>
         <OutputPreset>
            <Version>2.0</Version>
            <Name>DNxHD 36</Name>
            <ColorModel>YCC 709</ColorModel>
            <BitDepth>8</BitDepth>
            <Format>1080 24p</Format>
            <Compression>DNxHD 36</Compression>
            <Conversion>Letterbox (center)</Conversion>
            <VideoFileType>.mxf</VideoFileType>
            <IsDefault>false</IsDefault>
         </OutputPreset>
         <Eye></Eye>
         <Scene></Scene>
         <Comment></Comment>
      </Transcode>
   </Group>
</MetaFuze_BatchTranscode>""",
            """<?xml version='1.0' encoding='UTF-8'?>
<MetaFuze_BatchTranscode xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="MetaFuzeBatchTranscode.xsd">
   <Configuration>
      <Local>8</Local>
      <Remote>8</Remote>
   </Configuration>
   <Group>
      <FileList>
         <File>/tmp/SEQ001_HSNI_003_0020_v001.mov</File>
      </FileList>
      <Transcode>
         <Version>1.0</Version>
         <File>/tmp/SEQ001_HSNI_003_0020_v001.mxf</File>
         <ClipName>SEQ001_HSNI_003_0020_v001</ClipName>
         <ProjectName>SEQ001_HSNI_003</ProjectName>
         <TapeName>SEQ001_HSNI_003_0020_v001</TapeName>
         <TC_Start>00:00:00:00</TC_Start>
         <DropFrame>false</DropFrame>
         <EdgeTC>** TimeCode N/A **</EdgeTC>
         <FilmType>35.4</FilmType>
         <KN_Start>AAAAAAAA-0000+00</KN_Start>
         <Frames>29</Frames>
         <Width>1024</Width>
         <Height>778</Height>
         <PixelRatio>1.0000</PixelRatio>
         <UseFilmInfo>false</UseFilmInfo>
         <UseTapeInfo>true</UseTapeInfo>
         <AudioChannelCount>0</AudioChannelCount>
         <UseMXFAudio>false</UseMXFAudio>
         <UseWAVAudio>false</UseWAVAudio>
         <SrcBitsPerChannel>8</SrcBitsPerChannel>
         <OutputPreset>DNxHD 36</OutputPreset>
         <OutputPreset>
            <Version>2.0</Version>
            <Name>DNxHD 36</Name>
            <ColorModel>YCC 709</ColorModel>
            <BitDepth>8</BitDepth>
            <Format>1080 24p</Format>
            <Compression>DNxHD 36</Compression>
            <Conversion>Letterbox (center)</Conversion>
            <VideoFileType>.mxf</VideoFileType>
            <IsDefault>false</IsDefault>
         </OutputPreset>
         <Eye></Eye>
         <Scene></Scene>
         <Comment></Comment>
      </Transcode>
   </Group>
</MetaFuze_BatchTranscode>""",
            """<?xml version='1.0' encoding='UTF-8'?>
<MetaFuze_BatchTranscode xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="MetaFuzeBatchTranscode.xsd">
   <Configuration>
      <Local>8</Local>
      <Remote>8</Remote>
   </Configuration>
   <Group>
      <FileList>
         <File>/tmp/SEQ001_HSNI_003_0030_v001.mov</File>
      </FileList>
      <Transcode>
         <Version>1.0</Version>
         <File>/tmp/SEQ001_HSNI_003_0030_v001.mxf</File>
         <ClipName>SEQ001_HSNI_003_0030_v001</ClipName>
         <ProjectName>SEQ001_HSNI_003</ProjectName>
         <TapeName>SEQ001_HSNI_003_0030_v001</TapeName>
         <TC_Start>00:00:00:00</TC_Start>
         <DropFrame>false</DropFrame>
         <EdgeTC>** TimeCode N/A **</EdgeTC>
         <FilmType>35.4</FilmType>
         <KN_Start>AAAAAAAA-0000+00</KN_Start>
         <Frames>44</Frames>
         <Width>1024</Width>
         <Height>778</Height>
         <PixelRatio>1.0000</PixelRatio>
         <UseFilmInfo>false</UseFilmInfo>
         <UseTapeInfo>true</UseTapeInfo>
         <AudioChannelCount>0</AudioChannelCount>
         <UseMXFAudio>false</UseMXFAudio>
         <UseWAVAudio>false</UseWAVAudio>
         <SrcBitsPerChannel>8</SrcBitsPerChannel>
         <OutputPreset>DNxHD 36</OutputPreset>
         <OutputPreset>
            <Version>2.0</Version>
            <Name>DNxHD 36</Name>
            <ColorModel>YCC 709</ColorModel>
            <BitDepth>8</BitDepth>
            <Format>1080 24p</Format>
            <Compression>DNxHD 36</Compression>
            <Conversion>Letterbox (center)</Conversion>
            <VideoFileType>.mxf</VideoFileType>
            <IsDefault>false</IsDefault>
         </OutputPreset>
         <Eye></Eye>
         <Scene></Scene>
         <Comment></Comment>
      </Transcode>
   </Group>
</MetaFuze_BatchTranscode>""",
        ]

        result = s.to_metafuze_xml()

        self.maxDiff = None
        self.assertEqual(
            expected_xmls[0],
            result[0]
        )
        self.assertEqual(
            expected_xmls[1],
            result[1]
        )
        self.assertEqual(
            expected_xmls[2],
            result[2]
        )