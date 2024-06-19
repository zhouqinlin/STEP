class unionFind:
  def __init__(self,n):
    self.par = [-1]*n
    self.rank = [0]*n
    self.size = [1]*n
  
  def root(self,x):
    if self.par[x]==-1: return x
    else:
      self.par[x] = self.root(self.par[x])
      return self.par[x]
    
  def unite(self,x,y):
    x = self.root(x)
    y = self.root(y)
    if x==y: return False
    if self.rank[x]<self.rank[y]:
      x,y = y,x
    if self.rank[x]==self.rank[y]:
      self.rank[x] += 1
    self.size[x] += self.size[y]
    self.par[y] = x
    return True
  
  def same(self,x,y):
    return self.root(x)==self.root(y)
  
