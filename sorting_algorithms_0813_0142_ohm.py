# 代码生成时间: 2025-08-13 01:42:45
# sorting_algorithms.py
# 改进用户体验

"""
This module provides implementations of common sorting algorithms.
It is designed to be clear, maintainable, and extensible.
# 改进用户体验
"""

from typing import List, TypeVar

T = TypeVar('T')

def bubble_sort(arr: List[T]) -> List[T]:
    """A simple comparison-based sorting algorithm.
    It repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order.
    
    Args:
        arr (List[T]): A list of elements to sort.
    
    Returns:
        List[T]: The sorted list.
    
    Raises:
        TypeError: If the input is not a list.
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a list.")
    
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def selection_sort(arr: List[T]) -> List[T]:
# TODO: 优化性能
    """A sorting algorithm that divides the input list into a sorted and an unsorted region,
# 改进用户体验
    and repeatedly selects the smallest (or largest, depending on the ordering) element from the unsorted region and moves it to the sorted region.
    
    Args:
        arr (List[T]): A list of elements to sort.
    
    Returns:
        List[T]: The sorted list.
    
    Raises:
# 扩展功能模块
        TypeError: If the input is not a list.
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a list.")
    
    for i in range(len(arr)):
        min_index = i
# NOTE: 重要实现细节
        for j in range(i+1, len(arr)):
            if arr[min_index] > arr[j]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr
# 改进用户体验


def insertion_sort(arr: List[T]) -> List[T]:
    """A simple sorting algorithm that builds the final sorted array one item at a time.
    It is much less efficient on large lists than more advanced algorithms such as quicksort, heapsort, or merge sort.
# 扩展功能模块
    
    Args:
# 优化算法效率
        arr (List[T]): A list of elements to sort.
    
    Returns:
# FIXME: 处理边界情况
        List[T]: The sorted list.
# TODO: 优化性能
    
    Raises:
        TypeError: If the input is not a list.
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a list.")
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
# 优化算法效率
            j -= 1
        arr[j + 1] = key
    return arr

# Example usage:
if __name__ == '__main__':
    unsorted_list = [64, 34, 25, 12, 22, 11, 90]
    print("Unsorted list:", unsorted_list)
# FIXME: 处理边界情况
    sorted_list = bubble_sort(unsorted_list.copy())  # Using copy to avoid modifying the original list
    print("Sorted list (Bubble Sort): ", sorted_list)
# TODO: 优化性能
    sorted_list = selection_sort(unsorted_list.copy())
# 改进用户体验
    print("Sorted list (Selection Sort): ", sorted_list)
    sorted_list = insertion_sort(unsorted_list.copy())
    print("Sorted list (Insertion Sort): ", sorted_list)