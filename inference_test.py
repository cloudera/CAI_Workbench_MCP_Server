import os
import numpy as np
import xgboost as xgb
import mlflow
import mlflow.xgboost
from mlflow.models.signature import infer_signature
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from dotenv import load_dotenv

load_dotenv()

host = os.environ.get("CAI_WORKBENCH_HOST", "").rstrip("/")
api_key = os.environ.get("CAI_WORKBENCH_API_KEY")

# Try to set up MLflow to point to CAI
# In CML, MLflow Tracking URI is typically the host + some project specific path, or just host.
# Let's try the CML documentation pattern if we know it.
# Usually it's something like: https://<cml-host>/
os.environ["MLFLOW_TRACKING_URI"] = host
os.environ["MLFLOW_TRACKING_TOKEN"] = api_key

print("="*60)
print("Creating XGBoost Model for Registry")
print("="*60)

# ============================================================================
# 1. Generate Synthetic Dataset
# ============================================================================
print("\n1️⃣ Creating dataset...")
X, y = make_classification(
    n_samples=1000,
    n_features=20,
    n_informative=15,
    n_classes=2,
    random_state=42
)

X = X.astype(np.float32)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"✅ Train shape: {X_train.shape}, dtype: {X_train.dtype}")
print(f"✅ Test shape: {X_test.shape}, dtype: {X_test.dtype}")

# ============================================================================
# 2. Train XGBoost Model
# ============================================================================
print("\n2️⃣ Training XGBoost model...")
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

params = {
    'objective': 'binary:logistic',
    'max_depth': 4,
    'learning_rate': 0.1,
    'eval_metric': 'logloss',
    'seed': 42
}

model = xgb.train(
    params, 
    dtrain, 
    num_boost_round=100,
    evals=[(dtest, 'test')],
    verbose_eval=False
)

y_pred = model.predict(dtest)
accuracy = accuracy_score(y_test, (y_pred > 0.5).astype(int))
print(f"✅ Model accuracy: {accuracy:.4f}")

# ============================================================================
# 3. Create MLflow Signature
# ============================================================================
print("\n3️⃣ Creating signature...")

sample_input = X_train[:5]
sample_output = model.predict(xgb.DMatrix(sample_input))

signature = infer_signature(sample_input, sample_output)

print(f"✅ Signature:")
print(f"   Inputs: {signature.inputs}")
print(f"   Outputs: {signature.outputs}")

# ============================================================================
# 4. Log to MLflow Registry
# ============================================================================
print("\n4️⃣ Logging to registry...")
try:
    mlflow.set_experiment("xgboost-mcp")

    with mlflow.start_run(run_name="xgboost-test") as run:
        mlflow.xgboost.log_model(
            xgb_model=model,
            artifact_path="model",
            signature=signature,
            input_example=X_train[:3],
            registered_model_name="xgboost-mcp",
        )

        mlflow.log_metrics({
            "accuracy": accuracy,
            "num_features": 20
        })

        run_id = run.info.run_id
        experiment_id = run.info.experiment_id
        print(f"✅ Model logged! Run ID: {run_id}, Experiment ID: {experiment_id}")

        with open("run_info.json", "w") as f:
            import json
            json.dump({"run_id": run_id, "experiment_id": experiment_id}, f)

    print("\n" + "="*60)
    print("✅ XGBoost Model Registered!")
    print("="*60)
    print("\nFor UI deployment:")
    print("   Registry model name: xgboost-mcp")
    print("   Format: AUTO-DETECTED as PYTHON_ML")
    print("   Runtime: cmlserving-python-runtime")
    print("   Flavor: xgboost (auto-detected)")
except Exception as e:
    print(f"Error logging to MLflow: {e}")
