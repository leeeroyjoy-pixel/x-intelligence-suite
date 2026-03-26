#!/usr/bin/env python3
from __future__ import annotations


def filter_candidates(candidates: list[dict], config: dict, runtime: dict) -> list[dict]:
    selection = config.get('selection', {})
    out = []
    for item in candidates:
        text = item.get('text', '') or ''
        if selection.get('drop_replies', True) and item.get('is_reply'):
            continue
        if selection.get('drop_retweets', True) and item.get('is_retweet'):
            continue
        if any(k in text for k in selection.get('exclude_keywords', []) or []):
            continue
        out.append(item)
    return out


def score_candidate(item: dict, config: dict) -> float:
    text = item.get('text', '')
    score = 0.0
    selection = config.get('selection', {})
    for k in selection.get('priority_keywords', []) or []:
        if k in text:
            score += 3
    if 'http' in text:
        score += 1
    if item.get('is_reply'):
        score -= 3
    likes = int(item.get('likes', 0) or 0)
    score += min(likes // 200, 3)
    if selection.get('prefer_media_posts', True) and item.get('media'):
        score += 1
    return score


def summarize_item(item: dict, config: dict) -> str:
    text = item.get('text', '')
    if 'debut' in text or 'announcement' in text:
        return '这是典型的launch/新人announcement型内容，属于当天最值得跟进的宣发信号。'
    if 'free' in text or 'event' in text or 'live' in text:
        return '这条偏活动转化，重点在引导报名、到店或线下参与。'
    if 'early access' in text or 'release' in text:
        return '这条属于发售/先行上线信息，适合归入作品上线节奏观察。'
    return '这条内容可作为该账号当天的代表更新，用于观察当前主推主题与宣发方向。'


def select_items(candidates: list[dict], config: dict) -> list[dict]:
    scored = [(score_candidate(it, config), it) for it in candidates]
    scored.sort(key=lambda x: x[0], reverse=True)
    max_items = config.get('selection', {}).get('max_items', 6)
    max_per_source = config.get('selection', {}).get('max_items_per_source', 2)
    selected = []
    per_source = {}
    for score, item in scored:
        if score < 1:
            continue
        handle = item['handle']
        if per_source.get(handle, 0) >= max_per_source:
            continue
        selected.append((score, item))
        per_source[handle] = per_source.get(handle, 0) + 1
        if len(selected) >= max_items:
            break
    return [it for _, it in selected]


def build_report_items(selected: list[dict], config: dict) -> list[dict]:
    items = []
    for idx, item in enumerate(selected, 1):
        items.append({
            'rank': idx,
            'handle': item['handle'],
            'post_id': item['post_id'],
            'url': item['url'],
            'title': '重点更新',
            'raw_text': item.get('text', ''),
            'summary_zh': summarize_item(item, config),
            'likes': item.get('likes', 0),
            'views': item.get('views', ''),
            'media_files': [],
            'embedded_media_files': [],
            'score': score_candidate(item, config),
            'tags': [],
        })
    return items
