(module
  (memory (export "memory") 1)
  (func (export "add") (param i32 i32) (result i32)
    local.get 0
    local.get 1
    i32.add)
  (func (export "spin")
    (loop br 0))
  (func (export "grow_to_pages") (param i32) (result i32)
    local.get 0
    memory.grow)
)
