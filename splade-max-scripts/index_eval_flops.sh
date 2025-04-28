# вычисление индекса + evaluation + flops! 
export PYTHONPATH=$PYTHONPATH:$(pwd)
export SPLADE_CONFIG_NAME="ru-splade-max.yaml" 


# Get lambda_d value from command line argument
if [ -z "$1" ]; then
    echo "Error: lambda_d parameter is required"
    echo "Usage: $0 <lambda_d>"
    echo "Example: $0 0.0001" 
    exit 1
fi

LAMBDA_D=$1

if [ -z "$2" ]; then
    echo "Error: lambda_q parameter is required"
    echo "Usage: $0 <lambda_d> <lambda_q>"
    echo "Example: $0 0.0001 0.0001" 
    exit 1
fi

LAMBDA_Q=$2

if [ -z "$3" ]; then
    echo "Error: model type parameter is required"
    echo "Usage: $0 <lambda_d> <lambda_q> <model_type>"
    echo "Example: $0 0.0001 0.0001 vk"
    echo "         $0 0.0001 0.0001 ai-forever"
    exit 1
fi


if [ "$3" != "vk" ] && [ "$3" != "ai-forever" ]; then
    echo "Error: model_type must be either 'vk' or 'ai-forever'"
    exit 1
fi

MODEL_TYPE=$3

if [ "$MODEL_TYPE" = "vk" ]; then
    MODEL_NAME="deepvk/RuModernBERT-base"
else
    MODEL_NAME="ai-forever/ruBert-base"
fi



CHECKPOINT_DIR=models/${MODEL_TYPE}_ru-splade-max_${LAMBDA_D}_${LAMBDA_Q}/checkpoint
INDEX_DIR=models/${MODEL_TYPE}_ru-splade-max_${LAMBDA_D}_${LAMBDA_Q}/index
OUT_DIR=models/${MODEL_TYPE}_ru-splade-max_${LAMBDA_D}_${LAMBDA_Q}/out



# Check if checkpoint directory exists
if [ ! -d "$CHECKPOINT_DIR" ]; then
    echo "Error: Checkpoint directory does not exist: $CHECKPOINT_DIR"
    echo "Please train the model first using train_ru-splade-max.sh"
    exit 1
fi

python -m splade.index \
    +config.checkpoint_dir=$CHECKPOINT_DIR \
    +config.index_dir=$INDEX_DIR \
    +config.out_dir=$OUT_DIR \
    config.regularizer.FLOPS.lambda_q=$LAMBDA_Q \
    config.regularizer.FLOPS.lambda_d=$LAMBDA_D \
    init_dict.model_type_or_dir=$MODEL_NAME \
    config.tokenizer_type=$MODEL_NAME

if [ $? -ne 0 ]; then
    echo "Error: Indexing failed"
    exit 1
fi


python -m splade.retrieve \
    +config.checkpoint_dir=$CHECKPOINT_DIR \
    +config.index_dir=$INDEX_DIR \
    +config.out_dir=$OUT_DIR \
    config.regularizer.FLOPS.lambda_q=$LAMBDA_Q \
    config.regularizer.FLOPS.lambda_d=$LAMBDA_D \
    init_dict.model_type_or_dir=$MODEL_NAME \
    config.tokenizer_type=$MODEL_NAME

if [ $? -ne 0 ]; then
    echo "Error: Retrieval failed"
    exit 1
fi

python -m splade.flops \
    +config.checkpoint_dir=$CHECKPOINT_DIR \
    +config.index_dir=$INDEX_DIR \
    +config.out_dir=$OUT_DIR \
    config.regularizer.FLOPS.lambda_q=$LAMBDA_Q \
    config.regularizer.FLOPS.lambda_d=$LAMBDA_D \
    init_dict.model_type_or_dir=$MODEL_NAME \
    config.tokenizer_type=$MODEL_NAME

if [ $? -ne 0 ]; then
    echo "Error: FLOPS calculation failed"
    exit 1
fi

echo "Indexing, evaluation, and FLOPS calculation completed successfully"
exit 0
