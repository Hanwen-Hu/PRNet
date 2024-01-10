import argparse
import torch.cuda

from model import PRNet

hyper_para = argparse.ArgumentParser()
# Basic Settings
hyper_para.add_argument('-cuda_id', type=int, default=0)
hyper_para.add_argument('-batch_size', type=int, default=64)
hyper_para.add_argument('-epochs', type=int, default=100)
hyper_para.add_argument('-learning_rate', type=float, default=5e-4)
hyper_para.add_argument('-patience', type=int, default=10, help='Early Stopping')
hyper_para.add_argument('-load', type=str, default='False')
# Dataset Settings
hyper_para.add_argument('-dataset', type=str, default='Solar')
hyper_para.add_argument('-pred_scale', type=float, default=1)
dims = {'Electricity': 370, 'ETTh': 14, 'ETTm': 14, 'Exchange': 8, 'QPS': 10, 'Solar': 137, 'Traffic': 862,'Weather': 20}
patch_lens = {'Electricity': 96, 'ETTh': 24, 'ETTm': 96, 'Exchange': 30, 'QPS': 60, 'Solar': 288, 'Traffic': 24,'Weather': 144}
# Model Settings
embed_dims = {'Electricity': 32, 'ETTh': 16, 'ETTm': 16, 'Exchange': 16, 'QPS': 24, 'Solar': 32, 'Traffic': 24, 'Weather': 32}
hyper_para.add_argument('-layer_num', type=int, default=3, help='Number of Attention Layers')
hyper_para.add_argument('-patch_num', type=int, default=19, help='Number of Segments')
hyper_para.add_argument('-dropout', type=float, default=0.1, help='Dropout Probability')
args = hyper_para.parse_args()

args.patch_len = patch_lens[args.dataset]
args.seq_len = args.patch_len * 4
args.pred_len = int(patch_lens[args.dataset] * args.pred_scale)
args.embed_dim = embed_dims[args.dataset]
args.dim = dims[args.dataset]

if torch.cuda.is_available():
    args.device = torch.device('cuda', args.cuda_id)
else:
    args.device = torch.device('cpu')

if __name__ == '__main__':
    model = PRNet(args)
    model.count_parameter()
    model.train()
    model.test()
