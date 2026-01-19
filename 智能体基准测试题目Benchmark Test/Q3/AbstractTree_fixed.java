package com.inesa.ipms.api.common.support.tree;

import com.inesa.ipms.api.common.support.tree.node.TreeNode;
import com.inesa.ipms.framework.core.util.CollectionUtils;
import com.inesa.ipms.framework.core.util.ObjectUtils;
import lombok.Getter;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicReference;
import java.util.stream.Collectors;

/**
 * 通用树接口 - 修复版本
 * 修复了原始代码中的安全漏洞、性能问题和代码质量问题
 * @author : wangq
 * @since : 2025/4/11 15:14
 */
public abstract class AbstractTree<T extends TreeNode<T>> implements ITree<T> {

    private static final String DEFAULT_ROOT_NID = "0";
    private static final String DEFAULT_ROUTE_SEPARATOR = "-";
    
    @Getter
    private String rootNid = DEFAULT_ROOT_NID;
    
    @Getter
    private String routeSeparator = DEFAULT_ROUTE_SEPARATOR;
    
    // 修复：使用ConcurrentHashMap提高线程安全性
    private final Map<String, T> mapData = new ConcurrentHashMap<>();
    
    // 修复：使用volatile确保多线程可见性
    private volatile List<T> treeData = new ArrayList<>();

    /**
     * 查找node的行数据
     * @return node行数据集合
     */
    protected abstract List<T> getPureTreeNodes();

    @Override
    public List<T> getTree() {
        // 修复：返回不可修改的副本，防止外部修改内部状态
        return Collections.unmodifiableList(new ArrayList<>(this.treeData));
    }

    @Override
    public List<T> getList() {
        // 修复：返回不可修改的副本
        return Collections.unmodifiableList(new ArrayList<>(mapData.values()));
    }

    @Override
    public T getTreeNode(String nodeId) {
        // 修复：添加空值检查
        if (nodeId == null) {
            return null;
        }
        return mapData.get(nodeId);
    }

    @Override
    public List<T> getDescendantNodes(String nodeId, boolean isIncludeSelf) {
        // 修复：添加空值检查
        if (nodeId == null) {
            return Collections.emptyList();
        }
        
        List<T> descendants = new ArrayList<>();
        T currentNode = getTreeNode(nodeId);
        
        if (currentNode == null) {
            return descendants;
        }
        
        if (isIncludeSelf) {
            descendants.add(currentNode);
        }
        
        // 修复：使用迭代代替深度递归，防止栈溢出
        Deque<T> stack = new ArrayDeque<>();
        if (CollectionUtils.notEmpty(currentNode.getChildren())) {
            stack.addAll(currentNode.getChildren());
        }
        
        while (!stack.isEmpty()) {
            T node = stack.pop();
            descendants.add(node);
            
            if (CollectionUtils.notEmpty(node.getChildren())) {
                stack.addAll(node.getChildren());
            }
        }
        
        return descendants;
    }

    @Override
    public List<T> getAncestorNodes(String nodeId, boolean isIncludeSelf) {
        // 修复：添加空值检查
        if (nodeId == null) {
            return Collections.emptyList();
        }
        
        List<T> ancestors = new LinkedList<>();
        
        if (isIncludeSelf) {
            T selfNode = getTreeNode(nodeId);
            if (selfNode != null) {
                ancestors.add(0, selfNode);
            }
        }
        
        T currentNode = getTreeNode(nodeId);
        // 修复：添加循环检测，防止无限循环
        Set<String> visitedNodes = new HashSet<>();
        
        while (currentNode != null && currentNode.getPid() != null) {
            String parentId = currentNode.getPid();
            
            // 检测循环引用
            if (visitedNodes.contains(parentId)) {
                break; // 检测到循环引用，退出循环
            }
            visitedNodes.add(parentId);
            
            currentNode = getTreeNode(parentId);
            if (currentNode != null) {
                ancestors.add(0, currentNode);
            }
        }
        
        return ancestors;
    }

    @Override
    public List<T> filterTreeByNodeIds(List<String> nodeIds) {
        // 修复：添加空值检查
        if (CollectionUtils.isEmpty(nodeIds)) {
            return Collections.emptyList();
        }
        return filterTreeByNodeIds(this.treeData, nodeIds);
    }

    @Override
    public List<T> filterListByNodeIds(List<String> nodeIds) {
        // 修复：添加空值检查
        if (CollectionUtils.isEmpty(nodeIds)) {
            return Collections.emptyList();
        }
        List<T> filteredTree = filterTreeByNodeIds(nodeIds);
        return findAllNodes(filteredTree);
    }

    @Override
    public int sort(T t1, T t2) {
        // 修复：添加空值检查
        if (t1 == null || t2 == null) {
            return 0;
        }
        return Integer.compare(t1.getSequence(), t2.getSequence());
    }

    @Override
    public void refreshTree() {
        // 修复：使用同步块确保线程安全
        synchronized (this) {
            this.treeData = new ArrayList<>();
            this.mapData.clear();
            initializeTree();
        }
    }

    /**
     * 初始化树
     */
    protected void initializeTree() {
        List<T> rawTreeNodes = new ArrayList<>(getPureTreeNodes());
        
        // 修复：添加数据验证
        validateTreeNodes(rawTreeNodes);
        
        // 构建列表结构，方便快速查询节点
        this.mapData.clear();
        rawTreeNodes.forEach(s -> {
            if (s != null && s.getId() != null) {
                this.mapData.put(s.getId(), s);
            }
        });
        
        // 构建树结构
        this.treeData = buildTree(rawTreeNodes);
    }
    
    /**
     * 验证树节点数据的有效性
     * @param nodes 待验证的节点列表
     */
    private void validateTreeNodes(List<T> nodes) {
        if (CollectionUtils.isEmpty(nodes)) {
            return;
        }
        
        Set<String> nodeIds = new HashSet<>();
        for (T node : nodes) {
            if (node == null) {
                throw new IllegalArgumentException("树节点不能为null");
            }
            
            String nodeId = node.getId();
            if (nodeId == null || nodeId.trim().isEmpty()) {
                throw new IllegalArgumentException("节点ID不能为空");
            }
            
            if (nodeIds.contains(nodeId)) {
                throw new IllegalArgumentException("发现重复的节点ID: " + nodeId);
            }
            
            nodeIds.add(nodeId);
        }
    }

    /**
     * 第一次构建树，需要确认根路径是否为虚拟节点
     */
    private List<T> buildTree(List<T> allNodes) {
        String rootNid = getRootNid();
        AtomicReference<List<T>> result = new AtomicReference<>(new ArrayList<>());
        
        allNodes.stream()
                .filter(s -> s != null && s.getId() != null && s.getId().equals(rootNid))
                .findFirst()
                .ifPresentOrElse(s -> {
                    allNodes.remove(s);
                    List<T> children = buildTree(allNodes, s.getId());
                    s.setChildren(children.isEmpty() ? null : children);
                    result.set(new ArrayList<>() {{
                        add(s);
                    }});
                }, () -> result.set(buildTree(allNodes, rootNid)));
        
        return result.get();
    }

    /**
     * 递归构建树形结构
     * @param allNodes 所有待构建的节点列表
     * @param parentId 当前层级的父节点ID（为null时表示根节点）
     * @return 构建好的树形节点列表
     */
    private List<T> buildTree(List<T> allNodes, String parentId) {
        // 1. 找出当前层级的所有子节点
        List<T> currentLevelNodes = allNodes.stream()
                .filter(node -> node != null && Objects.equals(parentId, node.getPid()))
                .collect(Collectors.toList());

        // 2. 从原始列表中移除已找到的节点，提高后续递归效率
        allNodes.removeAll(currentLevelNodes);

        // 3. 递归构建每个子节点的子树
        currentLevelNodes.forEach(node -> {
            List<T> children = buildTree(allNodes, node.getId());
            node.setChildren(children.isEmpty() ? null : children);
        });

        // 4. 对当前层级节点排序（如有必要）
        if (CollectionUtils.notEmpty(currentLevelNodes)) {
            currentLevelNodes.sort(this::sort);
        }
        return currentLevelNodes;
    }

    /**
     * 根据节点过滤树
     * @param treeData 原始树
     * @param nodeIds  要过滤的节点
     * @return 子树
     */
    private List<T> filterTreeByNodeIds(List<T> treeData, List<String> nodeIds) {
        if (CollectionUtils.isEmpty(treeData) || CollectionUtils.isEmpty(nodeIds)) {
            return Collections.emptyList();
        }
        
        // 修复：使用深度复制避免修改原始数据
        List<T> cloneTreeData = deepCloneTree(treeData);
        Set<String> retainNodeIds = new HashSet<>();
        
        nodeIds.forEach(id -> {
            if (id != null) {
                Optional.ofNullable(getTreeNode(id)).ifPresent(s -> {
                    if (s.getRoute() != null) {
                        String[] path2 = s.getRoute().split(getRouteSeparator());
                        retainNodeIds.addAll(Arrays.asList(path2));
                    }
                });
            }
        });
        
        // 定义返回结果
        List<T> filteredTreeData = new ArrayList<>(cloneTreeData);
        if (CollectionUtils.notEmpty(retainNodeIds)) {
            retainTreeNodes(filteredTreeData, retainNodeIds);
        } else {
            filteredTreeData = new ArrayList<>();
        }
        
        return filteredTreeData;
    }
    
    /**
     * 深度克隆树结构
     * @param treeData 原始树数据
     * @return 克隆后的树数据
     */
    private List<T> deepCloneTree(List<T> treeData) {
        if (CollectionUtils.isEmpty(treeData)) {
            return new ArrayList<>();
        }
        
        List<T> clonedTree = new ArrayList<>();
        for (T node : treeData) {
            if (node != null) {
                T clonedNode = ObjectUtils.clone(node);
                if (clonedNode != null && CollectionUtils.notEmpty(node.getChildren())) {
                    clonedNode.setChildren(deepCloneTree(node.getChildren()));
                }
                clonedTree.add(clonedNode);
            }
        }
        
        return clonedTree;
    }

    /**
     * 将tree减枝，仅保留有效节点
     */
    private void retainTreeNodes(List<T> list, Set<String> filterNodeIds) {
        Iterator<T> iterator = list.iterator();
        while (iterator.hasNext()) {
            T node = iterator.next();
            if (node == null || !filterNodeIds.contains(node.getId())) {
                iterator.remove();
            } else if (CollectionUtils.notEmpty(node.getChildren())) {
                List<T> children = node.getChildren();
                if (CollectionUtils.notEmpty(children)) {
                    retainTreeNodes(children, filterNodeIds);
                }
            }
        }
    }

    /**
     * 循环查询所有节点
     * @param treeData 源tree结构
     * @return 列表
     */
    private List<T> findAllNodes(List<T> treeData) {
        List<T> list = new ArrayList<>();
        
        if (CollectionUtils.isEmpty(treeData)) {
            return list;
        }
        
        // 修复：使用迭代代替递归，防止栈溢出
        Deque<T> stack = new ArrayDeque<>(treeData);
        
        while (!stack.isEmpty()) {
            T node = stack.pop();
            if (node != null) {
                list.add(node);
                
                if (CollectionUtils.notEmpty(node.getChildren())) {
                    stack.addAll(node.getChildren());
                }
            }
        }
        
        return list;
    }
    
    /**
     * 新增：获取树的大小（节点数量）
     * @return 树中节点的总数
     */
    public int size() {
        return mapData.size();
    }
    
    /**
     * 新增：检查树是否为空
     * @return 如果树为空返回true，否则返回false
     */
    public boolean isEmpty() {
        return mapData.isEmpty();
    }
    
    /**
     * 新增：清除所有树数据
     */
    public void clear() {
        synchronized (this) {
            this.treeData.clear();
            this.mapData.clear();
        }
    }
}