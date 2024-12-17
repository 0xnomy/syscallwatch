#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <sys/user.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>

#define LOG_FILE "syscall_report.txt"

// Mock syscall names for demonstration.
const char *syscall_names[] = {
    "read", "write", "open", "close", "stat", "fstat", "lstat",
    "poll", "lseek", "mmap", "mprotect", "munmap", "brk", "rt_sigaction",
    "rt_sigprocmask", "rt_sigreturn", "ioctl", "pread64", "pwrite64", "readv",
    "writev", "access", "pipe", "select", "sched_yield", "mremap"};

// Struct to hold stats
typedef struct
{
    int known_syscalls;
    int unknown_syscalls;
} SyscallStats;

// Func to log messages to a file
void log_message(FILE *log, const char *message)
{
    fprintf(log, "%s\n", message);
}

// Func for summary
void generate_summary(FILE *log, SyscallStats stats)
{
    fprintf(log, "\n--- Summary ---\n");
    fprintf(log, "Total system calls traced: %d\n", stats.known_syscalls + stats.unknown_syscalls);
    fprintf(log, "Known system calls: %d\n", stats.known_syscalls);
    fprintf(log, "Unknown system calls: %d\n", stats.unknown_syscalls);
    fprintf(log, "Detailed log is available above.\n");
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s <target_program>\n", argv[0]);
        return 1;
    }

    pid_t child_pid = fork();
    if (child_pid < 0)
    {
        perror("Fork failed");
        return 1;
    }

    if (child_pid == 0)
    {
        // Child process
        printf("[Child] Starting target program: %s\n", argv[1]);
        ptrace(PTRACE_TRACEME, 0, NULL, NULL);
        execlp(argv[1], argv[1], NULL); // Replace child with target program
        perror("[Child] execlp failed");
        exit(1);
    }
    else
    {
        // Parent process (tracer)
        printf("[Parent] Tracing child process (PID: %d)\n", child_pid);

        struct user_regs_struct regs;
        int status;
        int syscall_count = sizeof(syscall_names) / sizeof(syscall_names[0]);

        // Open log file
        FILE *log = fopen(LOG_FILE, "w");
        if (!log)
        {
            perror("Failed to open log file");
            return 1;
        }

        // Initialize stats
        SyscallStats stats = {0, 0};

        waitpid(child_pid, &status, 0); // Wait for child to stop
        while (WIFSTOPPED(status))
        {
            if (ptrace(PTRACE_GETREGS, child_pid, NULL, &regs) == -1)
            {
                perror("[Parent] PTRACE_GETREGS failed");
                break;
            }

            // Identify the system call
            long syscall_num = regs.orig_rax;
            char log_message_buffer[256];

            if (syscall_num >= 0 && syscall_num < syscall_count)
            {
                stats.known_syscalls++;
                snprintf(log_message_buffer, sizeof(log_message_buffer),
                         "System call: %s (number: %ld)", syscall_names[syscall_num], syscall_num);
                printf("[Parent] %s\n", log_message_buffer);
            }
            else
            {
                stats.unknown_syscalls++;
                snprintf(log_message_buffer, sizeof(log_message_buffer),
                         "Unknown system call (number: %ld)", syscall_num);
                printf("[Parent] %s\n", log_message_buffer);
            }

            log_message(log, log_message_buffer);

            if (ptrace(PTRACE_SYSCALL, child_pid, NULL, NULL) == -1)
            {
                perror("[Parent] PTRACE_SYSCALL failed");
                break;
            }

            waitpid(child_pid, &status, 0);
        }

        printf("[Parent] Detaching from child process\n");
        ptrace(PTRACE_DETACH, child_pid, NULL, NULL);

        generate_summary(log, stats);
        fclose(log);

        printf("\n--- Summary ---\n");
        printf("Total system calls traced: %d\n", stats.known_syscalls + stats.unknown_syscalls);
        printf("Known system calls: %d\n", stats.known_syscalls);
        printf("Unknown system calls: %d\n", stats.unknown_syscalls);
        printf("Detailed report saved to '%s'\n", LOG_FILE);
    }

    return 0;
}
