var splitTemplate = 
`<div class="card">
    <div class="card-header" v-bind:id="headingId">
    <h2 class="mb-0">
        <button
            class="btn btn-link"
            type="button"
            data-toggle="collapse"
            v-bind:data-target="'#' + split.id"
            aria-expanded="true"
            v-bind:aria-controls="split.id">
        {{split.name}}
        </button>
    </h2>
    </div>
    <div
        v-bind:id="split.id"
        class="collapse"
        v-bind:aria-labelledby="headingId"
        v-bind:data-parent="'#' + accordionId">
    <div class="card-body">
        <table class="table table-bordered table-striped table-sm table-nonfluid">
        <thead>
            <tr>
            <th>Split</th>
            <th v-for="runner in runners">{{runner}}</th>
            </tr>
        </thead>
        <subsplit
            v-for="subsplit in split.subsplits"
            v-bind:runners="runners"
            v-bind:splitid="split.id"
            v-bind:subsplit="subsplit"
            v-bind:key="subsplit.to">
        </subsplit>
        </table>
    </div>
    </div>
</div>`;

var subsplitTemplate =
`<tr>
    <td>
    From: {{subsplit.from}}<br>
    To: {{subsplit.to}}
    </td>
    <clip
        v-for="clip in subsplit.clips"
        v-bind:clip="clip"
        v-bind:key="clip.id"
        v-bind:color="computeColor(clip.time)">
    </clip>
</tr>`;

var clipTemplate = 
`<td>
    <button
        v-bind:class="'btn ' + color + ' collapsed'"
        type="button"
        data-toggle="collapse"
        v-bind:data-target="'#' + clip.id"
        aria-expanded="false"
        v-bind:aria-controls="clip.id"
        v-bind:disabled="clip.time === null">
    {{clipTime}}
    </button>
    <div v-if="clip.time" v-bind:id="clip.id" class="collapse" v-bind:aria-labelledby="clip.id"></div>
</td>`;

Vue.component('clip', {
    props: ['clip', 'color'],
    template: clipTemplate,
    computed: {
        clipTime: function() {
            if (this.clip.time) {
                return Number(this.clip.time).toFixed(2);
            }
            return "n/a";
        }
    }
});

Vue.component('subsplit', {
    props: ['runners', 'splitid', 'subsplit'],
    template: subsplitTemplate,
    computed: {
        times: function() {
            return this.subsplit.clips.map(clip => clip.time).filter(val => val !== null);
        },
        fastestTime: function() {
            return Math.min.apply(null, this.times);
        },
        slowestTime: function() {
            return Math.max.apply(null, this.times);
        }
    },
    methods: {
        computeColor: function(time) {
            if (time == null) {
                return "btn-secondary";
            }
            if (time == this.fastestTime) {
                return "btn-success";
            }
            if (time == this.slowestTime) {
                return "btn-danger";
            }
            return "btn-warning";
        }
    }
});

Vue.component('split', {
    props: ['accordionId', 'runners', 'split'],
    template: splitTemplate,
    computed: {
        headingId: function() {
            return this.split.id + "-heading";
        }
    }
});

export function loadApp(file, showSplit)
{
    $.getJSON(file, function(data) {
        var app = new Vue({
            el: '#app',
            data: data
        })
        
        var urls = {};
        data.splits.forEach(function(split) {
            split.subsplits.forEach(function(subsplit) {
                subsplit.clips.forEach(function(clip) {
                    if (clip.url) {
                        urls[clip.id] = clip.url;
                    }
                })
            })
        });

        $('#app').on('show.bs.collapse', function(e) {
            if (e.target.id in urls) {
                $(e.target).html('<iframe width="480" height="360" src="' + urls[e.target.id] +
                    '"></iframe>');
            }
        });

        $('#app').on('hidden.bs.collapse', function(e) {
            if (e.target.id in urls) {
                $(e.target).html('');
            }
        });

        $('#' + showSplit).collapse('show')
    })    
}
