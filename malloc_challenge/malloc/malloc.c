#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NUM_BINS 12

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *bins[NUM_BINS];
} my_heap_t;

my_heap_t my_heap;

int get_bin_index(size_t size) {
  int index = 0;
  size = (size + 7) & ~7;  // Round up to multiple of 8
  while (size > 8 && index < NUM_BINS - 1) {
    size >>= 1;
    index++;
  }
  return index;
}

void my_add_to_bin(my_metadata_t *metadata) {
  int index = get_bin_index(metadata->size);
  metadata->next = my_heap.bins[index];
  my_heap.bins[index] = metadata;
}

void my_remove_from_bin(my_metadata_t *metadata, int index, my_metadata_t *prev) {
  if (prev) {
    prev->next = metadata->next;
  } else {
    my_heap.bins[index] = metadata->next;
  }
  metadata->next = NULL;
}

void my_initialize() {
  for (int i = 0; i < NUM_BINS; i++) {
    my_heap.bins[i] = NULL;
  }
}

void *my_malloc(size_t size) {
  int bin_index = get_bin_index(size);
  my_metadata_t *best_fit = NULL;
  my_metadata_t *best_fit_prev = NULL;
  
  // Find the best fit block
  for (int i = bin_index; i < NUM_BINS; i++) {
    my_metadata_t *metadata = my_heap.bins[i];
    my_metadata_t *prev = NULL;
    while (metadata) {
      if (metadata->size >= size && (!best_fit || metadata->size < best_fit->size)) {
        best_fit = metadata;
        best_fit_prev = prev;
        if (metadata->size == size) break;  // Perfect fit
      }
      prev = metadata;
      metadata = metadata->next;
    }
    if (best_fit && best_fit->size == size) break;  // Perfect fit
  }

  if (!best_fit) {
    // Allocate new memory if no suitable block is found
    size_t buffer_size = 4096;
    while (buffer_size < size + sizeof(my_metadata_t)) {
      buffer_size *= 2;
    }
    best_fit = (my_metadata_t *)mmap_from_system(buffer_size);
    best_fit->size = buffer_size - sizeof(my_metadata_t);
    best_fit->next = NULL;
    my_add_to_bin(best_fit);
    return my_malloc(size);  // Try again with the new memory
  }

  // Remove the block from its bin
  my_remove_from_bin(best_fit, get_bin_index(best_fit->size), best_fit_prev);

  void *ptr = best_fit + 1;
  size_t remaining_size = best_fit->size - size;

  if (remaining_size > sizeof(my_metadata_t)) {
    // Split the block
    best_fit->size = size;
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    my_add_to_bin(new_metadata);
  }

  return ptr;
}

void my_free(void *ptr) {
  if (!ptr) return;
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  
  // Try to merge with adjacent free blocks
  for (int i = 0; i < NUM_BINS; i++) {
    my_metadata_t *prev = NULL;
    my_metadata_t *current = my_heap.bins[i];
    
    while (current) {
      if ((char *)current + current->size + sizeof(my_metadata_t) == (char *)metadata) {
        // Merge with the previous block
        my_remove_from_bin(current, i, prev);
        current->size += metadata->size + sizeof(my_metadata_t);
        metadata = current;
        break;
      } else if ((char *)metadata + metadata->size + sizeof(my_metadata_t) == (char *)current) {
        // Merge with the next block
        my_remove_from_bin(current, i, prev);
        metadata->size += current->size + sizeof(my_metadata_t);
        break;
      }
      prev = current;
      current = current->next;
    }
  }
  
  my_add_to_bin(metadata);
}

void my_finalize() {
  // Nothing to do here for now
}

void test() {
  // Add your test cases here
  assert(1 == 1);
}