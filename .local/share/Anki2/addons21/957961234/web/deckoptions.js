// node_modules/svelte/internal/index.mjs
function noop() {
}
function run(fn) {
  return fn();
}
function blank_object() {
  return Object.create(null);
}
function run_all(fns) {
  fns.forEach(run);
}
function is_function(thing) {
  return typeof thing === "function";
}
function safe_not_equal(a, b) {
  return a != a ? b == b : a !== b || (a && typeof a === "object" || typeof a === "function");
}
function is_empty(obj) {
  return Object.keys(obj).length === 0;
}
function subscribe(store, ...callbacks) {
  if (store == null) {
    return noop;
  }
  const unsub = store.subscribe(...callbacks);
  return unsub.unsubscribe ? () => unsub.unsubscribe() : unsub;
}
var tasks = new Set();
var is_hydrating = false;
function start_hydrating() {
  is_hydrating = true;
}
function end_hydrating() {
  is_hydrating = false;
}
function upper_bound(low, high, key, value) {
  while (low < high) {
    const mid = low + (high - low >> 1);
    if (key(mid) <= value) {
      low = mid + 1;
    } else {
      high = mid;
    }
  }
  return low;
}
function init_hydrate(target) {
  if (target.hydrate_init)
    return;
  target.hydrate_init = true;
  const children2 = target.childNodes;
  const m = new Int32Array(children2.length + 1);
  const p = new Int32Array(children2.length);
  m[0] = -1;
  let longest = 0;
  for (let i = 0; i < children2.length; i++) {
    const current = children2[i].claim_order;
    const seqLen = upper_bound(1, longest + 1, (idx) => children2[m[idx]].claim_order, current) - 1;
    p[i] = m[seqLen] + 1;
    const newLen = seqLen + 1;
    m[newLen] = i;
    longest = Math.max(newLen, longest);
  }
  const lis = [];
  const toMove = [];
  let last = children2.length - 1;
  for (let cur = m[longest] + 1; cur != 0; cur = p[cur - 1]) {
    lis.push(children2[cur - 1]);
    for (; last >= cur; last--) {
      toMove.push(children2[last]);
    }
    last--;
  }
  for (; last >= 0; last--) {
    toMove.push(children2[last]);
  }
  lis.reverse();
  toMove.sort((a, b) => a.claim_order - b.claim_order);
  for (let i = 0, j = 0; i < toMove.length; i++) {
    while (j < lis.length && toMove[i].claim_order >= lis[j].claim_order) {
      j++;
    }
    const anchor = j < lis.length ? lis[j] : null;
    target.insertBefore(toMove[i], anchor);
  }
}
function append(target, node) {
  if (is_hydrating) {
    init_hydrate(target);
    if (target.actual_end_child === void 0 || target.actual_end_child !== null && target.actual_end_child.parentElement !== target) {
      target.actual_end_child = target.firstChild;
    }
    if (node !== target.actual_end_child) {
      target.insertBefore(node, target.actual_end_child);
    } else {
      target.actual_end_child = node.nextSibling;
    }
  } else if (node.parentNode !== target) {
    target.appendChild(node);
  }
}
function insert(target, node, anchor) {
  if (is_hydrating && !anchor) {
    append(target, node);
  } else if (node.parentNode !== target || anchor && node.nextSibling !== anchor) {
    target.insertBefore(node, anchor || null);
  }
}
function detach(node) {
  node.parentNode.removeChild(node);
}
function text(data) {
  return document.createTextNode(data);
}
function space() {
  return text(" ");
}
function children(element) {
  return Array.from(element.childNodes);
}
var active_docs = new Set();
var current_component;
function set_current_component(component) {
  current_component = component;
}
var dirty_components = [];
var binding_callbacks = [];
var render_callbacks = [];
var flush_callbacks = [];
var resolved_promise = Promise.resolve();
var update_scheduled = false;
function schedule_update() {
  if (!update_scheduled) {
    update_scheduled = true;
    resolved_promise.then(flush);
  }
}
function add_render_callback(fn) {
  render_callbacks.push(fn);
}
function add_flush_callback(fn) {
  flush_callbacks.push(fn);
}
var flushing = false;
var seen_callbacks = new Set();
function flush() {
  if (flushing)
    return;
  flushing = true;
  do {
    for (let i = 0; i < dirty_components.length; i += 1) {
      const component = dirty_components[i];
      set_current_component(component);
      update(component.$$);
    }
    set_current_component(null);
    dirty_components.length = 0;
    while (binding_callbacks.length)
      binding_callbacks.pop()();
    for (let i = 0; i < render_callbacks.length; i += 1) {
      const callback = render_callbacks[i];
      if (!seen_callbacks.has(callback)) {
        seen_callbacks.add(callback);
        callback();
      }
    }
    render_callbacks.length = 0;
  } while (dirty_components.length);
  while (flush_callbacks.length) {
    flush_callbacks.pop()();
  }
  update_scheduled = false;
  flushing = false;
  seen_callbacks.clear();
}
function update($$) {
  if ($$.fragment !== null) {
    $$.update();
    run_all($$.before_update);
    const dirty = $$.dirty;
    $$.dirty = [-1];
    $$.fragment && $$.fragment.p($$.ctx, dirty);
    $$.after_update.forEach(add_render_callback);
  }
}
var outroing = new Set();
var outros;
function transition_in(block, local) {
  if (block && block.i) {
    outroing.delete(block);
    block.i(local);
  }
}
function transition_out(block, local, detach2, callback) {
  if (block && block.o) {
    if (outroing.has(block))
      return;
    outroing.add(block);
    outros.c.push(() => {
      outroing.delete(block);
      if (callback) {
        if (detach2)
          block.d(1);
        callback();
      }
    });
    block.o(local);
  }
}
var globals = typeof window !== "undefined" ? window : typeof globalThis !== "undefined" ? globalThis : global;
var boolean_attributes = new Set([
  "allowfullscreen",
  "allowpaymentrequest",
  "async",
  "autofocus",
  "autoplay",
  "checked",
  "controls",
  "default",
  "defer",
  "disabled",
  "formnovalidate",
  "hidden",
  "ismap",
  "loop",
  "multiple",
  "muted",
  "nomodule",
  "novalidate",
  "open",
  "playsinline",
  "readonly",
  "required",
  "reversed",
  "selected"
]);
function bind(component, name, callback) {
  const index = component.$$.props[name];
  if (index !== void 0) {
    component.$$.bound[index] = callback;
    callback(component.$$.ctx[index]);
  }
}
function create_component(block) {
  block && block.c();
}
function mount_component(component, target, anchor, customElement) {
  const { fragment, on_mount, on_destroy, after_update } = component.$$;
  fragment && fragment.m(target, anchor);
  if (!customElement) {
    add_render_callback(() => {
      const new_on_destroy = on_mount.map(run).filter(is_function);
      if (on_destroy) {
        on_destroy.push(...new_on_destroy);
      } else {
        run_all(new_on_destroy);
      }
      component.$$.on_mount = [];
    });
  }
  after_update.forEach(add_render_callback);
}
function destroy_component(component, detaching) {
  const $$ = component.$$;
  if ($$.fragment !== null) {
    run_all($$.on_destroy);
    $$.fragment && $$.fragment.d(detaching);
    $$.on_destroy = $$.fragment = null;
    $$.ctx = [];
  }
}
function make_dirty(component, i) {
  if (component.$$.dirty[0] === -1) {
    dirty_components.push(component);
    schedule_update();
    component.$$.dirty.fill(0);
  }
  component.$$.dirty[i / 31 | 0] |= 1 << i % 31;
}
function init(component, options, instance2, create_fragment2, not_equal, props, dirty = [-1]) {
  const parent_component = current_component;
  set_current_component(component);
  const $$ = component.$$ = {
    fragment: null,
    ctx: null,
    props,
    update: noop,
    not_equal,
    bound: blank_object(),
    on_mount: [],
    on_destroy: [],
    on_disconnect: [],
    before_update: [],
    after_update: [],
    context: new Map(parent_component ? parent_component.$$.context : options.context || []),
    callbacks: blank_object(),
    dirty,
    skip_bound: false
  };
  let ready = false;
  $$.ctx = instance2 ? instance2(component, options.props || {}, (i, ret, ...rest) => {
    const value = rest.length ? rest[0] : ret;
    if ($$.ctx && not_equal($$.ctx[i], $$.ctx[i] = value)) {
      if (!$$.skip_bound && $$.bound[i])
        $$.bound[i](value);
      if (ready)
        make_dirty(component, i);
    }
    return ret;
  }) : [];
  $$.update();
  ready = true;
  run_all($$.before_update);
  $$.fragment = create_fragment2 ? create_fragment2($$.ctx) : false;
  if (options.target) {
    if (options.hydrate) {
      start_hydrating();
      const nodes = children(options.target);
      $$.fragment && $$.fragment.l(nodes);
      nodes.forEach(detach);
    } else {
      $$.fragment && $$.fragment.c();
    }
    if (options.intro)
      transition_in(component.$$.fragment);
    mount_component(component, options.target, options.anchor, options.customElement);
    end_hydrating();
    flush();
  }
  set_current_component(parent_component);
}
var SvelteElement;
if (typeof HTMLElement === "function") {
  SvelteElement = class extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: "open" });
    }
    connectedCallback() {
      const { on_mount } = this.$$;
      this.$$.on_disconnect = on_mount.map(run).filter(is_function);
      for (const key in this.$$.slotted) {
        this.appendChild(this.$$.slotted[key]);
      }
    }
    attributeChangedCallback(attr, _oldValue, newValue) {
      this[attr] = newValue;
    }
    disconnectedCallback() {
      run_all(this.$$.on_disconnect);
    }
    $destroy() {
      destroy_component(this, 1);
      this.$destroy = noop;
    }
    $on(type, callback) {
      const callbacks = this.$$.callbacks[type] || (this.$$.callbacks[type] = []);
      callbacks.push(callback);
      return () => {
        const index = callbacks.indexOf(callback);
        if (index !== -1)
          callbacks.splice(index, 1);
      };
    }
    $set($$props) {
      if (this.$$set && !is_empty($$props)) {
        this.$$.skip_bound = true;
        this.$$set($$props);
        this.$$.skip_bound = false;
      }
    }
  };
}
var SvelteComponent = class {
  $destroy() {
    destroy_component(this, 1);
    this.$destroy = noop;
  }
  $on(type, callback) {
    const callbacks = this.$$.callbacks[type] || (this.$$.callbacks[type] = []);
    callbacks.push(callback);
    return () => {
      const index = callbacks.indexOf(callback);
      if (index !== -1)
        callbacks.splice(index, 1);
    };
  }
  $set($$props) {
    if (this.$$set && !is_empty($$props)) {
      this.$$.skip_bound = true;
      this.$$set($$props);
      this.$$.skip_bound = false;
    }
  }
};

// node_modules/svelte/store/index.mjs
var subscriber_queue = [];
function writable(value, start = noop) {
  let stop;
  const subscribers = [];
  function set(new_value) {
    if (safe_not_equal(value, new_value)) {
      value = new_value;
      if (stop) {
        const run_queue = !subscriber_queue.length;
        for (let i = 0; i < subscribers.length; i += 1) {
          const s = subscribers[i];
          s[1]();
          subscriber_queue.push(s, value);
        }
        if (run_queue) {
          for (let i = 0; i < subscriber_queue.length; i += 2) {
            subscriber_queue[i][0](subscriber_queue[i + 1]);
          }
          subscriber_queue.length = 0;
        }
      }
    }
  }
  function update2(fn) {
    set(fn(value));
  }
  function subscribe2(run2, invalidate = noop) {
    const subscriber = [run2, invalidate];
    subscribers.push(subscriber);
    if (subscribers.length === 1) {
      stop = start(set) || noop;
    }
    run2(value);
    return () => {
      const index = subscribers.indexOf(subscriber);
      if (index !== -1) {
        subscribers.splice(index, 1);
      }
      if (subscribers.length === 0) {
        stop();
        stop = null;
      }
    };
  }
  return { set, update: update2, subscribe: subscribe2 };
}

// Rewards.svelte
function create_default_slot_6(ctx) {
  let t;
  return {
    c() {
      t = text("Begin at straight of length");
    },
    m(target, anchor) {
      insert(target, t, anchor);
    },
    d(detaching) {
      if (detaching)
        detach(t);
    }
  };
}
function create_default_slot_5(ctx) {
  let t;
  return {
    c() {
      t = text("Base ease reward");
    },
    m(target, anchor) {
      insert(target, t, anchor);
    },
    d(detaching) {
      if (detaching)
        detach(t);
    }
  };
}
function create_default_slot_4(ctx) {
  let t;
  return {
    c() {
      t = text("Step ease reward");
    },
    m(target, anchor) {
      insert(target, t, anchor);
    },
    d(detaching) {
      if (detaching)
        detach(t);
    }
  };
}
function create_default_slot_3(ctx) {
  let t;
  return {
    c() {
      t = text("Start at ease");
    },
    m(target, anchor) {
      insert(target, t, anchor);
    },
    d(detaching) {
      if (detaching)
        detach(t);
    }
  };
}
function create_default_slot_2(ctx) {
  let t;
  return {
    c() {
      t = text("Stop at ease");
    },
    m(target, anchor) {
      insert(target, t, anchor);
    },
    d(detaching) {
      if (detaching)
        detach(t);
    }
  };
}
function create_default_slot_1(ctx) {
  let t;
  return {
    c() {
      t = text("Enable notification");
    },
    m(target, anchor) {
      insert(target, t, anchor);
    },
    d(detaching) {
      if (detaching)
        detach(t);
    }
  };
}
function create_default_slot(ctx) {
  let spinboxrow;
  let updating_value;
  let t0;
  let spinboxfloatrow0;
  let updating_value_1;
  let t1;
  let spinboxfloatrow1;
  let updating_value_2;
  let t2;
  let spinboxfloatrow2;
  let updating_value_3;
  let t3;
  let spinboxfloatrow3;
  let updating_value_4;
  let t4;
  let switchrow;
  let updating_value_5;
  let current;
  function spinboxrow_value_binding(value) {
    ctx[6](value);
  }
  let spinboxrow_props = {
    defaultValue: 2,
    markdownTooltip: "Length of what is considered a straight success. Starting at this length, ease rewards will be applied. The value 0 is the same as deactivating Straight Rewards.",
    $$slots: { default: [create_default_slot_6] },
    $$scope: { ctx }
  };
  if (ctx[1].straightLength !== void 0) {
    spinboxrow_props.value = ctx[1].straightLength;
  }
  spinboxrow = new ctx[3]({ props: spinboxrow_props });
  binding_callbacks.push(() => bind(spinboxrow, "value", spinboxrow_value_binding));
  function spinboxfloatrow0_value_binding(value) {
    ctx[7](value);
  }
  let spinboxfloatrow0_props = {
    defaultValue: 0.05,
    markdownTooltip: "The ease reward is calculated as: BaseEase + StepEase \u22C5 (StraightLength - RequiredStraightLength)",
    $$slots: { default: [create_default_slot_5] },
    $$scope: { ctx }
  };
  if (ctx[1].baseEase !== void 0) {
    spinboxfloatrow0_props.value = ctx[1].baseEase;
  }
  spinboxfloatrow0 = new ctx[4]({ props: spinboxfloatrow0_props });
  binding_callbacks.push(() => bind(spinboxfloatrow0, "value", spinboxfloatrow0_value_binding));
  function spinboxfloatrow1_value_binding(value) {
    ctx[8](value);
  }
  let spinboxfloatrow1_props = {
    defaultValue: 0.05,
    markdownTooltip: "The ease reward is calculated as: BaseEase + StepEase \u22C5 (StraightLength - RequiredStraightLength)",
    $$slots: { default: [create_default_slot_4] },
    $$scope: { ctx }
  };
  if (ctx[1].stepEase !== void 0) {
    spinboxfloatrow1_props.value = ctx[1].stepEase;
  }
  spinboxfloatrow1 = new ctx[4]({ props: spinboxfloatrow1_props });
  binding_callbacks.push(() => bind(spinboxfloatrow1, "value", spinboxfloatrow1_value_binding));
  function spinboxfloatrow2_value_binding(value) {
    ctx[9](value);
  }
  let spinboxfloatrow2_props = {
    defaultValue: 1.3,
    markdownTooltip: "Only cards with an ease factor between (inclusive) *Start Ease* and *Stop Ease* are considered for ease rewards.",
    $$slots: { default: [create_default_slot_3] },
    $$scope: { ctx }
  };
  if (ctx[1].startEase !== void 0) {
    spinboxfloatrow2_props.value = ctx[1].startEase;
  }
  spinboxfloatrow2 = new ctx[4]({ props: spinboxfloatrow2_props });
  binding_callbacks.push(() => bind(spinboxfloatrow2, "value", spinboxfloatrow2_value_binding));
  function spinboxfloatrow3_value_binding(value) {
    ctx[10](value);
  }
  let spinboxfloatrow3_props = {
    defaultValue: 2.5,
    markdownTooltip: "Only cards with an ease factor between (inclusive) *Start Ease* and *Stop Ease* are considered for ease rewards.",
    $$slots: { default: [create_default_slot_2] },
    $$scope: { ctx }
  };
  if (ctx[1].stopEase !== void 0) {
    spinboxfloatrow3_props.value = ctx[1].stopEase;
  }
  spinboxfloatrow3 = new ctx[4]({ props: spinboxfloatrow3_props });
  binding_callbacks.push(() => bind(spinboxfloatrow3, "value", spinboxfloatrow3_value_binding));
  function switchrow_value_binding(value) {
    ctx[11](value);
  }
  let switchrow_props = {
    defaultValue: true,
    markdownTooltip: "Enable or disable the notifications that arise during review.",
    $$slots: { default: [create_default_slot_1] },
    $$scope: { ctx }
  };
  if (ctx[1].enableNotification !== void 0) {
    switchrow_props.value = ctx[1].enableNotification;
  }
  switchrow = new ctx[5]({ props: switchrow_props });
  binding_callbacks.push(() => bind(switchrow, "value", switchrow_value_binding));
  return {
    c() {
      create_component(spinboxrow.$$.fragment);
      t0 = space();
      create_component(spinboxfloatrow0.$$.fragment);
      t1 = space();
      create_component(spinboxfloatrow1.$$.fragment);
      t2 = space();
      create_component(spinboxfloatrow2.$$.fragment);
      t3 = space();
      create_component(spinboxfloatrow3.$$.fragment);
      t4 = space();
      create_component(switchrow.$$.fragment);
    },
    m(target, anchor) {
      mount_component(spinboxrow, target, anchor);
      insert(target, t0, anchor);
      mount_component(spinboxfloatrow0, target, anchor);
      insert(target, t1, anchor);
      mount_component(spinboxfloatrow1, target, anchor);
      insert(target, t2, anchor);
      mount_component(spinboxfloatrow2, target, anchor);
      insert(target, t3, anchor);
      mount_component(spinboxfloatrow3, target, anchor);
      insert(target, t4, anchor);
      mount_component(switchrow, target, anchor);
      current = true;
    },
    p(ctx2, dirty) {
      const spinboxrow_changes = {};
      if (dirty & 4096) {
        spinboxrow_changes.$$scope = { dirty, ctx: ctx2 };
      }
      if (!updating_value && dirty & 2) {
        updating_value = true;
        spinboxrow_changes.value = ctx2[1].straightLength;
        add_flush_callback(() => updating_value = false);
      }
      spinboxrow.$set(spinboxrow_changes);
      const spinboxfloatrow0_changes = {};
      if (dirty & 4096) {
        spinboxfloatrow0_changes.$$scope = { dirty, ctx: ctx2 };
      }
      if (!updating_value_1 && dirty & 2) {
        updating_value_1 = true;
        spinboxfloatrow0_changes.value = ctx2[1].baseEase;
        add_flush_callback(() => updating_value_1 = false);
      }
      spinboxfloatrow0.$set(spinboxfloatrow0_changes);
      const spinboxfloatrow1_changes = {};
      if (dirty & 4096) {
        spinboxfloatrow1_changes.$$scope = { dirty, ctx: ctx2 };
      }
      if (!updating_value_2 && dirty & 2) {
        updating_value_2 = true;
        spinboxfloatrow1_changes.value = ctx2[1].stepEase;
        add_flush_callback(() => updating_value_2 = false);
      }
      spinboxfloatrow1.$set(spinboxfloatrow1_changes);
      const spinboxfloatrow2_changes = {};
      if (dirty & 4096) {
        spinboxfloatrow2_changes.$$scope = { dirty, ctx: ctx2 };
      }
      if (!updating_value_3 && dirty & 2) {
        updating_value_3 = true;
        spinboxfloatrow2_changes.value = ctx2[1].startEase;
        add_flush_callback(() => updating_value_3 = false);
      }
      spinboxfloatrow2.$set(spinboxfloatrow2_changes);
      const spinboxfloatrow3_changes = {};
      if (dirty & 4096) {
        spinboxfloatrow3_changes.$$scope = { dirty, ctx: ctx2 };
      }
      if (!updating_value_4 && dirty & 2) {
        updating_value_4 = true;
        spinboxfloatrow3_changes.value = ctx2[1].stopEase;
        add_flush_callback(() => updating_value_4 = false);
      }
      spinboxfloatrow3.$set(spinboxfloatrow3_changes);
      const switchrow_changes = {};
      if (dirty & 4096) {
        switchrow_changes.$$scope = { dirty, ctx: ctx2 };
      }
      if (!updating_value_5 && dirty & 2) {
        updating_value_5 = true;
        switchrow_changes.value = ctx2[1].enableNotification;
        add_flush_callback(() => updating_value_5 = false);
      }
      switchrow.$set(switchrow_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(spinboxrow.$$.fragment, local);
      transition_in(spinboxfloatrow0.$$.fragment, local);
      transition_in(spinboxfloatrow1.$$.fragment, local);
      transition_in(spinboxfloatrow2.$$.fragment, local);
      transition_in(spinboxfloatrow3.$$.fragment, local);
      transition_in(switchrow.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(spinboxrow.$$.fragment, local);
      transition_out(spinboxfloatrow0.$$.fragment, local);
      transition_out(spinboxfloatrow1.$$.fragment, local);
      transition_out(spinboxfloatrow2.$$.fragment, local);
      transition_out(spinboxfloatrow3.$$.fragment, local);
      transition_out(switchrow.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(spinboxrow, detaching);
      if (detaching)
        detach(t0);
      destroy_component(spinboxfloatrow0, detaching);
      if (detaching)
        detach(t1);
      destroy_component(spinboxfloatrow1, detaching);
      if (detaching)
        detach(t2);
      destroy_component(spinboxfloatrow2, detaching);
      if (detaching)
        detach(t3);
      destroy_component(spinboxfloatrow3, detaching);
      if (detaching)
        detach(t4);
      destroy_component(switchrow, detaching);
    }
  };
}
function create_fragment(ctx) {
  let titledcontainer;
  let current;
  titledcontainer = new ctx[2]({
    props: {
      title: "Rewards",
      $$slots: { default: [create_default_slot] },
      $$scope: { ctx }
    }
  });
  return {
    c() {
      create_component(titledcontainer.$$.fragment);
    },
    m(target, anchor) {
      mount_component(titledcontainer, target, anchor);
      current = true;
    },
    p(ctx2, [dirty]) {
      const titledcontainer_changes = {};
      if (dirty & 4098) {
        titledcontainer_changes.$$scope = { dirty, ctx: ctx2 };
      }
      titledcontainer.$set(titledcontainer_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(titledcontainer.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(titledcontainer.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(titledcontainer, detaching);
    }
  };
}
function instance($$self, $$props, $$invalidate) {
  let $data, $$unsubscribe_data = noop, $$subscribe_data = () => ($$unsubscribe_data(), $$unsubscribe_data = subscribe(data, ($$value) => $$invalidate(1, $data = $$value)), data);
  $$self.$$.on_destroy.push(() => $$unsubscribe_data());
  const { TitledContainer, SpinBoxRow, SpinBoxFloatRow, SwitchRow } = anki.components;
  let { data } = $$props;
  $$subscribe_data();
  function spinboxrow_value_binding(value) {
    if ($$self.$$.not_equal($data.straightLength, value)) {
      $data.straightLength = value;
      data.set($data);
    }
  }
  function spinboxfloatrow0_value_binding(value) {
    if ($$self.$$.not_equal($data.baseEase, value)) {
      $data.baseEase = value;
      data.set($data);
    }
  }
  function spinboxfloatrow1_value_binding(value) {
    if ($$self.$$.not_equal($data.stepEase, value)) {
      $data.stepEase = value;
      data.set($data);
    }
  }
  function spinboxfloatrow2_value_binding(value) {
    if ($$self.$$.not_equal($data.startEase, value)) {
      $data.startEase = value;
      data.set($data);
    }
  }
  function spinboxfloatrow3_value_binding(value) {
    if ($$self.$$.not_equal($data.stopEase, value)) {
      $data.stopEase = value;
      data.set($data);
    }
  }
  function switchrow_value_binding(value) {
    if ($$self.$$.not_equal($data.enableNotification, value)) {
      $data.enableNotification = value;
      data.set($data);
    }
  }
  $$self.$$set = ($$props2) => {
    if ("data" in $$props2)
      $$subscribe_data($$invalidate(0, data = $$props2.data));
  };
  return [
    data,
    $data,
    TitledContainer,
    SpinBoxRow,
    SpinBoxFloatRow,
    SwitchRow,
    spinboxrow_value_binding,
    spinboxfloatrow0_value_binding,
    spinboxfloatrow1_value_binding,
    spinboxfloatrow2_value_binding,
    spinboxfloatrow3_value_binding,
    switchrow_value_binding
  ];
}
var Rewards = class extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance, create_fragment, safe_not_equal, { data: 0 });
  }
};
var Rewards_default = Rewards;

// deckoptions.js
$deckOptions.then((deckOptions) => {
  const data = writable({
    straightLength: 1,
    baseEase: 0.05,
    stepEase: 0.05,
    startEase: 1.3,
    stopEase: 2.5,
    enableNotification: true
  });
  deckOptions.options.append({ component: Rewards_default, props: { data } }, -4);
});
