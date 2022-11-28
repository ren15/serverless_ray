# serverless_ray

Goal of this project:
- Provide a similar interface for serverless computing, just like using ray
- Similar to what modal.com did.
- Leverage AWS lambda, and K8s
- serverless
- parallel 
- DAG
- edge computing


## Code sample

`run_1.py` is the MVP code.

`run_2.py` is how it looks like when integrated with S3 and DAG.


## DAG

### Register DAG

```python
class Alpha:
    def __init__(self):
        pass
    def f1(self):
        return open + close
    def f2(self):
        return open - close
    def f3(self):
        return f1 + f2
```

```rust
struct Alpha{
}
impl Alpha{
    fn f1(& self){
        return self.open + self.close
    }
    fn f2(& self){
        return self.open - self.close
    }
    fn f3(& self){
        return self.f1 + self.f2
    }
}
```

We also need "deserialization" or "static reflection", i.e.
```rust
fn cal(name:String){
    match name{
        "f1" => f1(open,close),
        "f2" => f2(open,close),
        "f3" => f3(f1,f2),
    }
}
```

In rust, we also need high-performance tensor framework. Such as openmp binding, or mkl binding.

The framework should automatically reason that f3 depend on f1 and f2,
and issue error when there is a cycle or infeasible node.

### Parallel execution, lazy evaluation/update

Say 
```
A -> B -> C -|
     D -> E -|-> F
```
When D has an update, we need to recalculate E and F, but not A, B, C.
This is called "differential_dataflow".

An intuitive implementation is that, maintaining the "in-degree" list of nodes,
only compute(update) nodes with 0 in-degree, and handle it's out-degree neighers.
Use `rayon` to parrallel in iterating through vectors.


References
- https://docs.rs/differential-dataflow/latest/differential_dataflow/
- https://github.com/timelydataflow/differential-dataflow/blob/master/differentialdataflow.pdf
- https://github.com/TimelyDataflow/differential-dataflow
- https://www.reddit.com/r/rust/comments/9oo464/best_way_to_parallelize_a_dag/
- https://docs.rs/rayon/latest/rayon/
- https://gitlab.com/tendsinmende/dager/-/tree/master
- https://gitlab.com/tendsinmende/asyncgraph

### Data optimization/ static compilation before running

- C++ compiler optimization
- Rust compiler optimization
- Edge elimination/ expression template
