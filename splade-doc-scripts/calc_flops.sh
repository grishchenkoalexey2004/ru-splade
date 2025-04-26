# данный скрипт запускает вычисление flops для модели 

export PYTHONPATH=$PYTHONPATH:$(pwd)
export SPLADE_CONFIG_NAME="ru-splade-doc.yaml" 
  
# Get lambda_d value from command line argument
if [ -z "$1" ]; then
    echo "Error: lambda_d parameter is required"
    echo "Usage: $0 <lambda_d> <model_type>"
    echo "Example: $0 0.0001 vk"
    echo "         $0 0.0001 ai-forever"
    exit 1
fi

LAMBDA_D=$1

if [ -z "$2" ]; then
    echo "Error: model type parameter is required" 
    echo "Usage: $0 <lambda_d> <model_type>"
    echo "Example: $0 0.0001 vk"
    echo "         $0 0.0001 ai-forever"
    exit 1
fi

if [ "$2" != "vk" ] && [ "$2" != "ai-forever" ]; then
    echo "Error: model_type must be either 'vk' or 'ai-forever'"
    exit 1
fi

MODEL_TYPE=$2

if [ "$MODEL_TYPE" = "vk" ]; then
    MODEL_NAME="deepvk/RuModernBERT-base"
else
    MODEL_NAME="ai-forever/ruBert-base"
fi



#! No debug for evaluation! 

CHECKPOINT_DIR=models/${MODEL_TYPE}_ru-splade-doc_${LAMBDA_D}/checkpoint
INDEX_DIR=models/${MODEL_TYPE}_ru-splade-doc_${LAMBDA_D}/index
OUT_DIR=models/${MODEL_TYPE}_ru-splade-doc_${LAMBDA_D}/out


SEED=$((RANDOM % 1000))
python -m splade.flops \
        +config.checkpoint_dir=$CHECKPOINT_DIR \
        +config.index_dir=$INDEX_DIR \
        +config.out_dir=$OUT_DIR \
        config.regularizer.FLOPS.lambda_q=0.0000 \
        config.regularizer.FLOPS.lambda_d=$LAMBDA_D \
        +config.random_seed=$SEED \
        init_dict.model_type_or_dir=$MODEL_NAME \
        config.tokenizer_type=$MODEL_NAME
    exit $?
else
    exit 1
fi