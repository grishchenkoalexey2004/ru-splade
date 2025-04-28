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

if [ -z "$4" ]; then
    echo "Error: dataset name parameter is required"
    echo "Usage: $0 <lambda_d> <lambda_q> <model_type> <dataset_name>"
    echo "Example: $0 0.0001 0.0001 vk kaengreg/rus-scifact"
    echo "         $0 0.0001 0.0001 ai-forever kaengreg/rus-scifact"
    exit 1
fi


DATASET_NAME=$4
echo "Dataset name: $DATASET_NAME"

if [ "$DATASET_NAME" != "kaengreg/rus-scifact" ] && \
   [ "$DATASET_NAME" != "kaengreg/rubq" ] && \
   [ "$DATASET_NAME" != "kaengreg/rus-arguana" ] && \
   [ "$DATASET_NAME" != "kaengreg/rus-nfcorpus" ] && \
   [ "$DATASET_NAME" != "kaengreg/rus-tidiqa" ] && \
   [ "$DATASET_NAME" != "kaengreg/rus-xquad" ]; then
    echo "Error: dataset_name must be one of the following: kaengreg/rus-scifact, kaengreg/rubq, kaengreg/rus-arguana, kaengreg/rus-nfcorpus, kaengreg/rus-tidiqa, kaengreg/rus-xquad"
    exit 1
fi

DATASET_DIR=${OUT_DIR}/rusbeir/${DATASET_NAME}

echo "Dataset will be saved in: $DATASET_DIR"

if [ -d "$DATASET_DIR" ]; then
    echo "Dataset already exists! Exiting..."
    exit 1
fi


python -m splade.rusbeir_eval \
    +config.checkpoint_dir=$CHECKPOINT_DIR \
    +config.index_dir=$INDEX_DIR \
    +config.out_dir=$OUT_DIR \
    config.regularizer.FLOPS.lambda_q=$LAMBDA_Q \
    config.regularizer.FLOPS.lambda_d=$LAMBDA_D \
    init_dict.model_type_or_dir=$MODEL_NAME \
    config.tokenizer_type=$MODEL_NAME \
    +rusbeir.dataset=$DATASET_NAME

exit 0
