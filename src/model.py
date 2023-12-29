from pydantic import BaseModel
from typing import List, Any, Optional
import enum


class AuthorInfo(BaseModel):
    aid: int 
    author_type: str
    avatar: str
    comments: str
    is_following: bool
    nickname: str
    

class FullAuthorList(BaseModel):
    full_author_list: List[AuthorInfo] = None
    full_work_list:Optional[List[Any]] = None
    total: int = 0
    
    
class AuthorType(enum.Enum):
    AuthorDrawing   = "AuthorDrawing"
    AuthorStrategy  = "AuthorStrategy"
    AuthorCoser     = "AuthorCoser"
    AuthorOther     = "AuthorOther"
    

class VoteUsersInfo(BaseModel):
    aid: int
    avatar: str
    nickname: str
    vote_num: int
    
    
class VotesInfo(BaseModel):
    author_info: AuthorInfo
    top_vote_users:List[VoteUsersInfo]
    villa_redirect_link: str
    vote_num_gap: int
    work_info: Any
    

    
    