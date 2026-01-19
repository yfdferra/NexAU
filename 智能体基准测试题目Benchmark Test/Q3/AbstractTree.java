package com.inesa.ipms.api.common.support.tree;

import com.inesa.ipms.api.common.support.tree.node.TreeNode;
import com.inesa.ipms.framework.core.util.CollectionUtils;
import com.inesa.ipms.framework.core.util.ObjectUtils;
import lombok.Getter;

import java.util.*;
import java.util.concurrent.atomic.AtomicReference;
import java.util.stream.Collectors;

/**
 * 通用树接口
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
    private final Map<String, T> mapData = new HashMap<>();
    private List<T> treeData = new ArrayList<>();

    /**
     * 查找node的行数据
     * @return node行数据集合
     */
    protected abstract List<T> getPureTreeNodes();

    @Override
    public List<T> getTree() {
        return this.treeData;
    }

    @Override
    public List<T> getList() {
        return new ArrayList<>(mapData.values());
    }

    @Override
    public T getTreeNode(String nodeId) {
        return mapData.get(nodeId);
    }

    @Override
    public List<T> getDescendantNodes(String nodeId, boolean isIncludeSelf) {
        List<T> descendants = new ArrayList<>();
        T currentNode = getTreeNode(nodeId);
        if (currentNode != null) {
            if (isIncludeSelf) {
                descendants.add(currentNode);
            }
            if (CollectionUtils.notEmpty(currentNode.getChildren())) {
                currentNode.getChildren().forEach(child ->
                        descendants.addAll(getDescendantNodes(child.getId(), true)));
            }
        }
        return descendants;
    }

    @Override
    public List<T> getAncestorNodes(String nodeId, boolean isIncludeSelf) {
        List<T> ancestors = new LinkedList<>();
        T currentNode = getTreeNode(nodeId);
        if (isIncludeSelf) {
            T selfNode = getTreeNode(nodeId);
            if (selfNode != null) {
                ancestors.add(0, selfNode);
            }
        }
        while (currentNode != null && currentNode.getPid() != null) {
            currentNode = getTreeNode(currentNode.getPid());
            if (currentNode != null) {
                ancestors.add(0, currentNode);
            }
        }
        return ancestors;
    }

    @Override
    public List<T> filterTreeByNodeIds(List<String> nodeIds) {
        return filterTreeByNodeIds(this.treeData, nodeIds);
    }

    @Override
    public List<T> filterListByNodeIds(List<String> nodeIds) {
        List<T> filteredTree = filterTreeByNodeIds(nodeIds);
        return findAllNodes(filteredTree);
    }

    @Override
    public int sort(T t1, T t2) {
        return t1.getSequence() - t2.getSequence();
    }

    @Override
    public void refreshTree() {
        this.treeData = new ArrayList<>();
        this.mapData.clear();
        initializeTree();
    }

    /**
     * 初始化树
     */
    protected void initializeTree() {
        List<T> rawTreeNodes = new ArrayList<>(getPureTreeNodes());
        //构建列表结构，方便快速查询节点
        this.mapData.clear();
        rawTreeNodes.forEach(s -> this.mapData.put(s.getId(), s));
        //构建树结构
        this.treeData = buildTree(rawTreeNodes);
    }

    /**
     * 第一次构建树，需要确认根路径是否为虚拟节点
     */
    private List<T> buildTree(List<T> allNodes) {
        String rootNid = getRootNid();
        AtomicReference<List<T>> result = new AtomicReference<>(new ArrayList<>());
        allNodes.stream().filter(s -> s.getId().equals(rootNid)).findFirst()
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
                .filter(node -> Objects.equals(parentId, node.getPid()))
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
        if (CollectionUtils.isEmpty(treeData)) {
            return Collections.emptyList();
        } else {
            List<T> cloneTreeData = ObjectUtils.clone(treeData);
            Set<String> retainNodeIds = new HashSet<>();
            nodeIds.forEach(id -> Optional.ofNullable(getTreeNode(id)).ifPresent(s -> {
                String[] path2 = s.getRoute().split(getRouteSeparator());
                retainNodeIds.addAll(List.of(path2));
            }));
            //定义返回结果
            List<T> filteredTreeData = new ArrayList<>(cloneTreeData);
            if (CollectionUtils.notEmpty(retainNodeIds)) {
                retainTreeNodes(filteredTreeData, retainNodeIds);
            } else {
                filteredTreeData = new ArrayList<>();
            }
            return filteredTreeData;
        }
    }

    /**
     * 将tree减枝，仅保留有效节点
     */
    private void retainTreeNodes(List<T> list, Set<String> filterNodeIds) {
        Iterator<T> iterator = list.iterator();
        while (iterator.hasNext()) {
            T node = iterator.next();
            if (!filterNodeIds.contains(node.getId())) {
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
        treeData.forEach(t -> {
            list.add(t);
            if (CollectionUtils.notEmpty(t.getChildren())) {
                list.addAll(findAllNodes(t.getChildren()));
            }
        });
        return list;
    }
}