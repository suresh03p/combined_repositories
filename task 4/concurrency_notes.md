# Concurrency Notes

This document summarizes core concurrency concepts, including processes, threads, synchronization, and parallel programming in Python.

## 1. Process vs Thread
- A process is an independent program with its own memory space.
- A thread is a lightweight execution unit inside a process and shares memory with other threads in the same process.

## 2. Concurrency vs Parallelism
- Concurrency means multiple tasks make progress over time by interleaving execution.
- Parallelism means multiple tasks run at the same time on different CPU cores.

## 3. Python GIL
- The GIL limits Python threads from executing bytecode in parallel.
- It is less harmful for I/O-bound tasks and more harmful for CPU-bound tasks.

## 4. CPU-bound vs I/O-bound
- CPU-bound tasks need more processing power.
- I/O-bound tasks wait on external resources such as files, network, or databases.

## 5. Synchronization
- Synchronization protects shared resources using locks, semaphores, or events.

## 6. Race Conditions
- Race conditions occur when multiple threads/processes access shared data without proper coordination.

## 7. Deadlocks
- Deadlocks happen when threads wait on each other indefinitely.
