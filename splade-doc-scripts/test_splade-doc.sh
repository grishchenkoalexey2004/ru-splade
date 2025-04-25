if [ -z "$1" ]; then
    echo "Error: lambda_d parameter is required"
    echo "Usage: $0 <lambda_d>"
    echo "Example: $0 0.0001" 
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


# все указанные пути используются исключительно для определения пути к модели 
CHECKPOINT_DIR=models/${MODEL_TYPE}_ru-splade-doc_${LAMBDA_D}/checkpoint
INDEX_DIR=models/${MODEL_TYPE}_ru-splade-doc_${LAMBDA_D}/index
OUT_DIR=models/${MODEL_TYPE}_ru-splade-doc_${LAMBDA_D}/out





python -m splade.test_model $CHECKPOINT_DIR $INDEX_DIR $OUT_DIR

exit 0 



