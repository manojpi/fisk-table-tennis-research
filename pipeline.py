import mmcv
import decord
import numpy as np
from mmcv.transforms import TRANSFORMS, BaseTransform, to_tensor
from mmaction.structures import ActionDataSample


@TRANSFORMS.register_module()
class VIdeoInit(BaseTransform):
    def transform(self, results):
        container = decord.VideoReader(results['filename'])
        results['total_frames'] = len(container)
        results['video_reader'] = container
        return results


@TRANSFORMS.register_module()
class VideoSample(BaseTransform):

    def __init__(self, clip_len, num_clips, test_mode=False):
        self.clip_len = clip_len
        self.num_clips = num_clips
        self.test_mode = test_mode
    
    def transform(self, results):
        total_frames = results["total_frames"]
        interval = total_frames // self.clip_len

        if self.test_mode:
            np.random.seed(42)
        
        inds_of_all_clips = []
        for i in range(self.num_clips):
            bids = np.arange(self.clip_len) * interval
            offset = 